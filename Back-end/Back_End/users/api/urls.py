from django.urls import path
from .apis import UserViewSet, LoginView, ContactFormView

urlpatterns = [
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('users/', UserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
    path('users/<int:pk>/change_password/', UserViewSet.as_view({'put': 'change_password'}), name='change_password'),
    path('users/<int:pk>/edit/', UserViewSet.as_view({'patch': 'edit_user'}), name='user-edit'),
    path('users/<int:pk>/address/', UserViewSet.as_view({'get': 'list_user_address'}), name='user_address'),
    path('users/<int:pk>/edit_direction/', UserViewSet.as_view({'put': 'edit_user_direction'}), name='user_edit_direction'),
    path('users/<int:pk>/desactive/', UserViewSet.as_view({'put': 'deactivate_user'}), name='user_desactive'),
    path('register/', UserViewSet.as_view({'post': 'register'}), name='user-register'),
    path('users/<int:pk>/avatar/', UserViewSet.as_view({'post': 'update_avatar'}), name='user-update-avatar'),
    path('users/recover-account/', UserViewSet.as_view({'post': 'recover_account'}), name='recover-account'),
    path('contact/', ContactFormView.as_view({'post': 'send_email'}), name='contact-form'),
]