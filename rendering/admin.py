from django.contrib import admin
from django.template.defaultfilters import truncatechars

from . import models


def truncated(field, chars=100):
    def truncate(obj):
        return truncatechars(getattr(obj, field), chars)
    # Set the column header display name
    truncate.__name__ = field
    return truncate


@admin.register(models.EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):

    list_display = [
        '__str__',
        truncated('comments'),
        truncated('subject'),
        'context_schema',
        'created',
    ]

    list_filter = [
        'created',
    ]

    search_fields = [
        'name',
        'comments',
        'subject',
        'html',
        'text',
    ]


@admin.register(models.JSONSchema)
class JSONSchemaAdmin(admin.ModelAdmin):

    list_display = [
        '__str__',
        truncated('comments'),
        truncated('schema_id'),
        'created',
    ]

    list_filter = [
        'created',
    ]

    search_fields = [
        'name',
        'comments',
        'schema',
    ]
