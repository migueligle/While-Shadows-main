import base64
from django.forms import ValidationError
from rest_framework import viewsets, status
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from marks.models import marks
from products.models import Products
from .serializers import ProductsListSerializer, ProductsCreateUpdateSerializer
from rest_framework.decorators import action
from base.pagination import smallPagination
from products.api.filters import ProductFilterSet
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.viewsets import ReadOnlyModelViewSet

class StaffPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all().order_by('name')
    filter_class = ProductFilterSet
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = smallPagination

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

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductsListSerializer
        return ProductsCreateUpdateSerializer

    @action(detail=True, methods=['put'])
    def deactivate_product(self, request, pk):
        product = self.get_object()
        current_status = product.is_active
        product.is_active = not current_status
        product.save()
        
        if product.is_active:
            message = "Producto activado con éxito."
        else:
            message = "Producto desactivado con éxito."
        
        return Response({"message": message}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            mark_instance = serializer.validated_data.get('mark')
            image_one_base64 = request.data.get('image', None)
            image_two_base64 = request.data.get('image_two', None)
            image_three_base64 = request.data.get('image_three', None)
            if image_one_base64:
                image_one = base64.b64decode(image_one_base64)
                serializer.validated_data['image'] = image_one
            if image_two_base64:
                image_two = base64.b64decode(image_two_base64)
                serializer.validated_data['image_two'] = image_two
            if image_three_base64:
                image_three = base64.b64decode(image_three_base64)
                serializer.validated_data['image_three'] = image_three
            
            serializer.save(mark=mark_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        mark_instance = serializer.validated_data.get('mark')
        image_one_base64 = request.data.get('image', None)
        image_two_base64 = request.data.get('image_two', None)
        image_three_base64 = request.data.get('image_three', None)

        if image_one_base64:
            image_one_base64 = image_one_base64.split(";base64,")[-1]
            image_one = base64.b64decode(image_one_base64)
            serializer.validated_data['image'] = image_one
        if image_two_base64:
            image_two_base64 = image_two_base64.split(";base64,")[-1]
            image_two = base64.b64decode(image_two_base64)
            serializer.validated_data['image_two'] = image_two
        if image_three_base64:
            image_three_base64 = image_three_base64.split(";base64,")[-1]
            image_three = base64.b64decode(image_three_base64)
            serializer.validated_data['image_three'] = image_three

        serializer.save(mark=mark_instance)
        return Response(serializer.data)

class ReadOnlyOrIsAuthenticated(IsAuthenticated):
  
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated  and  request.user.is_staff 

class ProductsBaseViewSet(ReadOnlyModelViewSet):
    queryset = Products.objects.filter(is_active=True,is_stock=True).order_by('name')
    filter_class = ProductFilterSet
    serializer_class=ProductsListSerializer
    pagination_class = smallPagination

  
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

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


