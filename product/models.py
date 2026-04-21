from django.db import models
from django.utils.text import slugify

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    class Meta:
        abstract = True


class ProductCategory(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Product category: {self.name}"
    

class ProductUnitTypes(models.TextChoices):
    KG = 'kg', 'kilogram'
    DONA = 'dona','dona'
    G = 'g', 'gramm'
    METR = 'm', 'metr'
    ML = 'ml', 'ml'
    L = 'l', 'litr'


class Product(BaseModel):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveBigIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=25, default=ProductUnitTypes.DONA)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save()