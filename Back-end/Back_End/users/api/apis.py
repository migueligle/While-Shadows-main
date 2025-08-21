import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from datetime import datetime
from users.api.filters import UserFilterSet
from ..models import User
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer, UserAddressSerializer, UserAdminSerializer, UserAllSerializer, UserBaseSerializer, UserEditDirectionBaseSerializer, UserEditDirectionSerializer, UsereditSerializer
from base.pagination import smallPagination
import base64
from django.http import JsonResponse
import random
import unicodedata
import string


class ContactFormView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def send_email(self, request):
        data = request.data
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        subject = data.get('subject')

        if not all([name, email, phone, subject]):
            return Response({"error": "Todos los campos son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            
            with open(finders.find('images/logo.png'), 'rb') as image_file:
                image_data = image_file.read()
                image_base64 = base64.b64encode(image_data).decode('utf-8')
            html_content = render_to_string( 'users/contact.html', {
                'name': name,
                'email': email,
                'phone': phone,
                'subject': subject,
                'EMAIL_IMAGE_URL': image_base64
            })
            email_subject = f"Nuevo mensaje de contacto: {email}"
            from_email = f'{email}' 
            to_email = ['WhileShadows@gmail.com']  
            msg = EmailMultiAlternatives(email_subject, '', from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return Response({"success": "El correo electrónico se ha enviado correctamente."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"No se pudo enviar el correo electrónico: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = smallPagination
    filter_class = UserFilterSet 
    
   
    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            queryset = self.filter_queryset(self.get_queryset())
            if self.filter_class:
                queryset = self.filter_class(request.GET, queryset=queryset).qs
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = UserAdminSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = UserAdminSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated]) 
    def update_avatar(self, request, pk):
        user = self.get_object()
        if request.user == user or request.user.is_staff:
            avatar_file = request.data.get('file')
            if avatar_file:
                try:
                    avatar_data = avatar_file.read()
                    encoded_avatar = base64.b64encode(avatar_data)
                    user.avatar = base64.b64decode(encoded_avatar)
                    user.save()
                    return Response({"message": "Avatar actualizado correctamente."}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"error": f"No se pudo guardar la imagen: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "No se proporcionó ningún archivo de imagen."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "No tienes permiso para actualizar el avatar de este usuario."}, status=status.HTTP_403_FORBIDDEN)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff or request.user == instance:
            serializer = UserBaseSerializer(instance)
            return Response(serializer.data)
        else:
            return Response({"message": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated]) 
    def list_user_address(self, request, pk):
        user = self.get_object()
        if request.user == user or request.user.is_staff:
            serializer = UserAddressSerializer(user)
            return Response(serializer.data)
        else:
            return Response({"message": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff or request.user == instance:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'register':
            return RegisterSerializer
        elif self.action == 'edit_user_direction':
            return UserEditDirectionBaseSerializer
        else:
            return UserBaseSerializer

    def get_permissions(self):
        if self.action in ['deactivate_user','list_user_address','list','edit_user', 'retrieve', 'edit_user_direction','update_avatar','update','change_password']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'register', 'recover_account']:
            permission_classes = [AllowAny]  
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def edit_user_direction(self, request, pk):
        user = self.get_object()
        if request.user == user or request.user.is_staff:
            serializer = UserEditDirectionBaseSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:    
            return Response({"message": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        serializer.save(password=make_password(serializer.validated_data['password']))  

    @action(detail=True, methods=['put'])
    def deactivate_user(self, request, pk):
        user = self.get_object()
        if not (request.user == user or request.user.is_staff):
            return Response({"message": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        
        if user.is_active:
            user.is_active = False
            user.save()
            return Response({"message": "Usuario Desactivado con éxito"}, status=status.HTTP_200_OK)
        else:
            user.is_active = True
            user.save()
            return Response({"message": "Usuario Activado con éxito"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def change_password(self, request, pk):
        user = User.objects.get(id=pk)
        new_password = request.data.get('password')
        user.set_password(new_password)
        user.save()
        
        return Response({"message": "Contraseña cambiada con éxito"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def edit_user(self, request, pk):
        user = self.get_object()      
        if not request.user.is_authenticated:
            return Response({"message": "No autorizado"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.user == user or request.user.is_staff:
            serializer = UsereditSerializer(user, data=request.data, partial=True)
            
            if request.user.is_staff and 'is_staff' in request.data:
                serializer.is_staff_read_only = False
            else:
                serializer.is_staff_read_only = True  
            if 'email' in request.data:
                email = request.data['email']
                if email == user.email:
                    serializer.fields['email'].required = False

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'])
    def recover_account(self,request):
        if request.method == 'POST':
            email = self.request.data['email']
            if email:
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    return JsonResponse({'error': 'KO'}, status=400)

                password_len = 10 
                unicode_characters = string.ascii_letters + string.digits + string.punctuation + '¡¿áéíóúñ'
                unicode_characters *= (password_len // len(unicode_characters)) + 1
                new_password = ''.join(random.choice(unicode_characters) for _ in range(password_len))
                new_password = unicodedata.normalize('NFKC', new_password)
                
                user.set_password(new_password)
                user.save()
                
                with open(finders.find('images/logo.png'), 'rb') as image_file:
                    image_data = image_file.read()
                    image_base64 = base64.b64encode(image_data).decode('utf-8')
                html_content = render_to_string('users/index.html', {'new_password': new_password,'EMAIL_IMAGE_URL': image_base64})

                subject = 'Recuperación de Contraseña'
                from_email = 'WhileShadows@gmail.com' 
                to_email = [email]
                msg = EmailMultiAlternatives(subject, '', from_email, to_email)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                
                return Response({'message': 'OK'}, status=200)
            else:
                return Response({'error': 'Falta el correo electrónico '}, status=400)
        else:
            return Response({'error': 'Método no permitido'}, status=405)

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
