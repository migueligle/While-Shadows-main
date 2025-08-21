from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

from Provinces.models import provinces

class ManagerUser(UserManager):
    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Debes introducir un correo electrónico")

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **kwargs):
        kwargs.setdefault("is_staff", False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email=None, password=None, **kwargs):
        kwargs.setdefault("is_staff", True)
        return self._create_user(email, password, **kwargs)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=100,unique=True)
    avatar = models.BinaryField() 
    name = models.CharField(max_length=100,blank=True, null=True)
    first_name = models.CharField(max_length=100,blank=True, null=True)
    last_name = models.CharField(max_length=100,blank=True, null=True)
    create_at = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    dni=models.CharField(max_length=9, blank=True, null=True)
    birthdate=models.DateField(blank=True, null=True,default=None)
    postal_code=models.CharField(max_length=15,blank=True, null=True,default=None)
    phone=models.CharField(max_length=18, blank=True, null=True)
    direction=models.CharField(max_length=255, blank=True, null=True)
    is_active=models.BooleanField(db_index=True,null=False,blank=False,default=True)
    locality = models.CharField(max_length=100,blank=True, null=True)
    province=models.ForeignKey(provinces, models.DO_NOTHING,blank=True, null=True,related_name='user')
    is_verified=models.BooleanField(db_index=True,null=False,blank=False,default=True)
    objects = ManagerUser()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["-create_at"]
        db_table = 'users'