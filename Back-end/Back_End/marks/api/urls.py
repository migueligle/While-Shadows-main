from django.urls import path
from .apis import MarksModelViewSet,MarksModelBaseViewSet

urlpatterns = [
    path('marks/', MarksModelViewSet.as_view({'get': 'list', 'post': 'create'}), name='marks-list'),
    path('marks-base/', MarksModelBaseViewSet.as_view({'get': 'list'}), name='marks-base'),
    path('marks/<int:pk>/', MarksModelViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='marks-detail'),
    path('marks/<int:pk>/deactivate/', MarksModelViewSet.as_view({'put': 'deactivate_mark'}), name='marks-deactivate'),
]
