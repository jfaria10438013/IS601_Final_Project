from django.db import models

# Create your models here.
class Item(models.Model):
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField()
    count = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    image = models.URLField(max_length=200, null=True, blank=True)  # Assuming it's a URL
    # If you want to store images locally, use an ImageField instead
    # image = models.ImageField(upload_to='item_images/', null=True, blank=True)

    def __str__(self):
        return self.name
