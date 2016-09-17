from django.db import models


class NoUpdateMixin:
    """Don't allow updates after creation.

    Doesn't prevent batch updates or other cases where save is not
    called -- use database permissions for robustness in those cases.
    """

    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # TODO: use an append-only postgres role
        if self.pk is not None:
            raise ValueError(
                "{} cannot be updated after creation."
                .format(self.__class__))
        return super().save(*args, **kwargs)


class AlwaysCopyOnWriteMixin(models.Model):
    """Create new instances instead of mutating existing ones.

    Doesn't prevent batch updates or other cases where save is not
    called -- use database permissions for robustness in those cases.
    """

    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # TODO: use an append-only postgres role
        self.pk = None
        super().save(*args, **kwargs)
