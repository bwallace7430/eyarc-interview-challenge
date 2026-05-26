from django.db import models


class SoftDeleteObject(models.Model):
    """Minimal stub — the real implementation adds soft-delete behaviour."""

    class Meta:
        abstract = True
