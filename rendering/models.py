import jsonschema
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from jsonschema import Draft4Validator

from render_liquid import render_liquid


class CopyOnWriteMixin(models.Model):
    """Create new instances instead of mutating existing ones.

    Doesn't prevent batch updates or other cases where save is not
    called -- use database permissions for robustness in those cases.
    """

    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)

    immutable_fields = ()

    def save(self, *args, **kwargs):
        # TODO: use an append-only postgres role
        if self.pk is not None:
            # We are updating an existing object
            prev = self.__class__.objects.get(pk=self.pk)
            if any(getattr(self, name) != getattr(prev, name)
                   for name in self.immutable_fields):
                self.pk = None
                # Make a note of this object's origin
                note = "Modified from {}".format(prev)
                if self.comments:
                    self.comments = note + '\n\n' + self.comments
                else:
                    self.comments = note
        super().save(*args, **kwargs)


class AutoCleanMixin:
    """Perform a full_clean on every save."""

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class JSONSchema(CopyOnWriteMixin, AutoCleanMixin, models.Model):
    name = models.CharField(max_length=254, blank=True)
    comments = models.TextField(blank=True)
    schema = JSONField(null=True, blank=True)

    class Meta:
        verbose_name = 'JSON schema'

    immutable_fields = ['schema']

    @property
    def schema_id(self):
        try:
            return self.schema['id']
        except Exception:
            return None

    @property
    def schema_version(self):
        try:
            return self.schema['$schema']
        except Exception:
            return None

    def validate(self, data):
        """Check if this schema describes the given data."""
        try:
            return jsonschema.validate(data, self.schema)
        except jsonschema.ValidationError as e:
            raise ValidationError(e.message)
        except Exception as e:
            raise ValidationError(e)

    def clean(self):
        try:
            Draft4Validator.check_schema(self.schema)
        except jsonschema.SchemaError as e:
            raise ValidationError(
                {'schema': "Invalid schema: {}".format(e.message)})
        # TODO: default "$schema": "http://json-schema.org/draft-04/schema#"

    def __str__(self):
        if self.name:
            return '{} (#{})'.format(self.name, self.id)
        else:
            return '{} #{}'.format(self.__class__.__name__, self.id)


class EmailTemplate(CopyOnWriteMixin, models.Model):
    name = models.CharField(max_length=254, blank=True)
    comments = models.TextField(blank=True)

    subject = models.TextField(blank=True)
    html = models.TextField(blank=True)
    text = models.TextField(blank=True)
    context_schema = models.ForeignKey('JSONSchema')
    # TODO: validate template syntax

    immutable_fields = [
        'subject',
        'html',
        'text',
        'context_schema',
    ]

    def __str__(self):
        if self.name:
            return '{} (#{})'.format(self.name, self.id)
        else:
            return '{} #{}'.format(self.__class__.__name__, self.id)

    def render(self, context, validate=True):
        if validate:
            self.context_schema.validate(context)
        return {name: render_liquid(getattr(self, name), context)
                for name in ['subject', 'html', 'text']}

# {
#     "$schema": "http://json-schema.org/draft-04/schema#",
#     "title": "Required variables",
#     "description": "Required replacement variables for a template",
#     "type": "array",
#     "items": {
#         "title": "Name",
#         "description": "The name of a template variable",
#         "type": "string"
#     },
#     "uniqueItems": true
# }
