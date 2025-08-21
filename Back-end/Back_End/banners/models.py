from django.db import models


class Banners(models.Model):
   name=models.CharField(max_length=120,unique=False)
   is_active = models.BooleanField(default=True)
   image= models.BinaryField(default=None) 
   class Meta:
    db_table = 'banners'
    
