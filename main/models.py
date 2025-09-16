from django.db import models

# Create your models here.
import uuid
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('shoes', 'Shoes'),
        ('jersey', 'Jersey'),
        ('equipment', 'Equipment'),
        ('accessories', 'Accessories'),
        ('training', 'Training'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='training')
    thumbnail = models.URLField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def is_popular(self):
        return self.views > 50  # contoh: produk dianggap populer jika sudah 50x dilihat

    def increment_views(self):
        self.views += 1
        self.save()