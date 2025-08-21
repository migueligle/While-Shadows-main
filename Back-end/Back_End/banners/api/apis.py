import base64
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from requests import Response
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from banners.api.filters import BannersFilter
from banners.api.serializers import BannersSerializer
from banners.models import Banners
from base.pagination import smallPagination
from rest_framework.decorators import action

class BannersBaseViewSet(viewsets.ModelViewSet):
    queryset = Banners.objects.filter(is_active=True).order_by('id')
    serializer_class = BannersSerializer
    permission_classes = []
    filter_class = BannersFilter 
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

class BannersViewSet(viewsets.ModelViewSet):
    queryset = Banners.objects.all().order_by('id')
    serializer_class = BannersSerializer
    filter_class = BannersFilter 
    ordering_fields = ['name']
    pagination_class = smallPagination
    permission_classes = [IsAuthenticated, IsAdminUser]

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
    def deactivate_banner(self, request, pk=None):
        banner = self.get_object()
        current_status = banner.is_active
        banner.is_active = not current_status
        banner.save()
        
        if banner.is_active:
            message = "Banner activado con éxito."
        else:
            message = "Banner desactivado con éxito."
        
        return Response({"message": message}, status=status.HTTP_200_OK)
