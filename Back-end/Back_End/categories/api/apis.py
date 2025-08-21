from django.urls import path
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import BasePermission
from base.pagination import smallPagination
from categories.api.filters import CategoriesFilterSet
from ..models import Categories
from .serializers import CategoriesSerializers
import base64
from django.core.files.base import ContentFile
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAuthenticated

class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

class CategoriesModelViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializers
    pagination_class = smallPagination
    filter_class = CategoriesFilterSet
    permission_classes = [IsAuthenticated, IsStaffUser]
    
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filterset = self.filter_class(request.query_params, queryset=queryset)
        queryset = filterset.qs
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response({"message": "ko"}, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_staff == True:
            return Response({"error": "No tienes permiso para crear categorías."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            image_one_base64 = request.data.get('image', None)
            
            if image_one_base64:
                image_data = image_one_base64.split(';base64,')[-1]
                image_data = base64.b64decode(image_data)
                serializer.validated_data['image'] = image_data
                
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff == True:
            return Response({"error": "No tienes permiso para actualizar categorías."}, status=status.HTTP_403_FORBIDDEN)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        image_one_base64 = request.data.get('image', None)
        
        if image_one_base64:
            image_one_base64 = image_one_base64.split(";base64,")[-1]
            image_one = base64.b64decode(image_one_base64)
            serializer.validated_data['image'] = image_one
        
        
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=True, methods=['put'])
    def deactivate_Categories(self, request, pk=None):
        if not request.user.is_staff == True:
            return Response({"error": "No tienes permiso para desactivar la categoría."}, status=status.HTTP_403_FORBIDDEN)
        category = self.get_object()
        current_status = category.is_active
        category.is_active = not current_status
        category.save()
        
        if category.is_active:
            message = "Categoría activado con éxito."
        else:
            message = "Categoría desactivado con éxito."
        
        return Response({"message": message}, status=status.HTTP_200_OK)

class CategoriesBaseModelViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.filter(is_active=True)
    serializer_class = CategoriesSerializers
    pagination_class = smallPagination
     
    def list(self, request, *args, **kwargs):
        queryset = Categories.objects.filter(is_active=True)
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response({"message": "ko"}, status=status.HTTP_400_BAD_REQUEST)