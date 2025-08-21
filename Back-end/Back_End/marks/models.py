from django.db import models

class marks(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active=models.BooleanField(default=True) 

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'marks'
        verbose_name = 'marks'
    