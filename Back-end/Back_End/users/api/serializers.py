import datetime
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from ..models import User
import pytz

class UsereditSerializer(serializers.ModelSerializer):
    birthdate = serializers.DateTimeField()

    class Meta:
        model = User
        fields = ("id", "email", "avatar", "name", "last_name", "create_at", "is_staff", "dni", "birthdate", "phone", "is_active", "avatar")
class UserBaseSerializer(serializers.ModelSerializer):
    birthdate = serializers.SerializerMethodField()

    def get_birthdate(self, user):
        birthdate = user.birthdate
        if birthdate:
            if isinstance(birthdate, datetime.date):
                birthdate = datetime.datetime.combine(birthdate, datetime.datetime.min.time())
            
            birthdate = birthdate.astimezone(pytz.utc)
            
            return birthdate.isoformat()
        return None

    class Meta:
        model = User
        fields = ("id", "email", "avatar", "name", "last_name", "create_at", "is_staff", "dni", "birthdate", "phone", "is_active", "avatar")

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['id'] = user.id
        token['is_staff'] = user.is_staff
        token['is_active'] = user.is_active
        token['name'] = user.name
        token['last_name'] = user.last_name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = authenticate(email=attrs['email'], password=attrs['password'])
        if user and not user.is_active:
            raise serializers.ValidationError()
        return data

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "password"]
        
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("El campo 'email' no puede estar vacío.")

        if "@" not in value or not value.endswith((".com", ".es")):
            raise serializers.ValidationError("El formato del correo electrónico no es válido.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("La contraseña debe contener al menos un número.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("La contraseña debe contener al menos una letra minúscula.")
        return make_password(value)


class UserEditDirectionSerializer(serializers.ModelSerializer):
    postal_code=serializers.IntegerField()
    direction=serializers.CharField()
    locality = serializers.CharField()
        
    class Meta:
        model = User
        fields = ("postal_code", "direction","locality","province")

class UserEditDirectionBaseSerializer(serializers.ModelSerializer):
    postal_code=serializers.IntegerField()
    direction=serializers.CharField()
    locality = serializers.CharField()

    
    class Meta:
        model = User
        fields = ("postal_code", "direction","locality","province")



class UserAddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("postal_code", "direction",'province',"locality")

class  UserAllSerializer(serializers.ModelSerializer):
    birthdate = serializers.DateTimeField()

    class Meta:
        model = User
        fields = ("postal_code", "direction",'province',"locality","id","email","avatar","name","last_name","create_at","is_staff","dni" ,"birthdate","phone","is_active","avatar")

class  UserAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("postal_code", "direction",'province',"locality","id","email","avatar","name","last_name","create_at","is_staff","dni" ,"phone","is_active","avatar",'birthdate')

