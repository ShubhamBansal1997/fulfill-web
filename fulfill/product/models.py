# Third Party Stuff
from django.db import models
from django.utils.translation import gettext_lazy as _

# fulfill Stuff
from fulfill.base.models import TimeStampedUUIDModel

# third party


# Create your models here.
class Product(TimeStampedUUIDModel):
    """
    Product Model
    """
    name = models.CharField(null=False, blank=False, max_length=250)
    sku = models.CharField(null=False, blank=False, unique=True, max_length=250)
    description = models.TextField(null=True)

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        self.sku = self.sku.lower()
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.sku)
