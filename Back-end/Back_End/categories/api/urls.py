from django.urls import path
from .apis import CategoriesModelViewSet,CategoriesBaseModelViewSet

urlpatterns = [
    path('categories/', CategoriesModelViewSet.as_view({'get': 'list', 'post': 'create'}), name='categories'),
    path('categories-base/', CategoriesBaseModelViewSet.as_view({'get': 'list'}), name='categories-base'),
    path('categories/<int:pk>/edit/', CategoriesModelViewSet.as_view({'put': 'update'}), name='category-edit'),
    path('categories/<int:pk>/deactivate/', CategoriesModelViewSet.as_view({'put': 'deactivate_Categories'}), name='categories-deactivate'),
]