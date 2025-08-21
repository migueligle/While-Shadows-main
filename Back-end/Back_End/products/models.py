from django.db import models
from categories.models import Categories
from marks.models import marks

class Products(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    before_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    characteristics = models.TextField()
    description = models.TextField()
    is_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    image= models.BinaryField(default=None,null=True, blank=True) 
    image_two= models.BinaryField(default=None,null=True, blank=True)
    image_three= models.BinaryField(default=None,null=True, blank=True)  
    mark = models.ForeignKey(marks, default=None ,related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Categories,default=None,related_name='products', on_delete=models.CASCADE)
    video= models.TextField(null=True, blank=True)


    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'products'
        verbose_name = "Product"
        verbose_name_plural = "Products"



