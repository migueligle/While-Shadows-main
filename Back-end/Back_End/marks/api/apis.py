from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from base.pagination import smallPagination
from marks.api.filters import MarkFilterSet
from marks.api.serializers import MarksSerializers
from ..models import marks
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, BasePermission
import base64

class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

class MarksModelViewSet(viewsets.ModelViewSet):
    queryset = marks.objects.all()
    serializer_class = MarksSerializers
    filter_class = MarkFilterSet
    pagination_class = smallPagination
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
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put'])
    def deactivate_mark(self, request, pk):
        mark = self.get_object()
        current_status = mark.is_active
        mark.is_active = not current_status
        mark.save()
        
        if mark.is_active:
            message = "Marca activado con éxito."
        else:
            message = "Marca desactivado con éxito."
        
        return Response({"message": message}, status=status.HTTP_200_OK)
    
class MarksModelBaseViewSet(viewsets.ModelViewSet):
    queryset = marks.objects.filter(is_active=True)
    serializer_class = MarksSerializers
    filter_class = MarkFilterSet
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
