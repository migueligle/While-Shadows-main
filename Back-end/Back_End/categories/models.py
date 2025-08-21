from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image= models.BinaryField(default=None)
    is_active=models.BooleanField(default=True) 

    def __str__(self):
        return self.name
    class  Meta: 
        db_table = 'categories'
        verbose_name = 'category'
    
