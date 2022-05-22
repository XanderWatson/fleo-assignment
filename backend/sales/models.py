from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Created model for tree-like hierarchy using MPTT model
class Category(MPTTModel):
    categoryName = models.CharField(max_length=50)
    categoryID = models.CharField(max_length=75, default='', blank=True, unique=True)
    targetSales = models.PositiveIntegerField(default=1)
    currentSales = models.PositiveIntegerField(default=0)
    progressPercentage = models.DecimalField(
        decimal_places=2, max_digits=5, default=0.00)
    progressColor = models.CharField(max_length=20, default="Red")
    parent = TreeForeignKey('self', on_delete=models.SET_NULL,
                            null=True, blank=True, related_name='children')

    def __str__(self) -> str:
        return self.categoryID

    class Meta:
        verbose_name_plural = "Categories"
