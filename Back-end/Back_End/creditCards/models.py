from django.db import models
from users.models import User

class CreditCards(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    last_four_digits = models.CharField(max_length=4)
    mark = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name
    
    class Meta:
        db_table = 'credit_Cards'
        verbose_name = "credit Card"
        verbose_name_plural = "credit Cards"
