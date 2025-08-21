from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission
from ..models import provinces
from .serializers import ProvincesSerializers

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['GET', 'HEAD', 'OPTIONS']

class ProvincesModelViewSet(viewsets.ModelViewSet):
    
    queryset = provinces.objects.all()
    serializer_class = ProvincesSerializers
    permission_classes = [ReadOnly]