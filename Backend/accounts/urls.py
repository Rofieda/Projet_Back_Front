from unicodedata import name
from django.urls import path
from .views import RegisterView, LoginUserView, LogoutAPIView, AddUserView, ListUsersView, DeleteUserView, \
    PasswordResetRequestView, PasswordResetConfirm, SetNewPasswordView, BloqueruserView, DebloqueruserView, \
    GestionUserView, UserProfileAPIView

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login-user'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('add-user/', AddUserView.as_view(), name='add_user'),
    path('list_users/', ListUsersView.as_view(), name='list_users'),
    path('users/<int:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='reset-password-confirm'),
    path('set-new-password/',SetNewPasswordView.as_view(), name='set-new-password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('bloqueuser/<int:pk>/', BloqueruserView.as_view(), name='bloquer-user'),
    path('débloqueuser/<int:pk>/', DebloqueruserView.as_view(), name='bloquer-user'),
    path('gestion-user/<int:pk>/', GestionUserView.as_view(), name='gestion-user'),
    path('user/<int:id>/', UserProfileAPIView.as_view(), name='user_profile'),
    ]
