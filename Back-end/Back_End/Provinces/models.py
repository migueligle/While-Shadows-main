from django.db import models


class provinces(models.Model):
   name=models.CharField(max_length=120,unique=False)
   class Meta:
    db_table = 'provinces'
    verbose_name = 'province'
    verbose_name_plural = 'provinces'
    
