from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login'
    ),

    path('logout/', views.cerrar_sesion, name='logout'),
    path('registro/', views.registro_bombero, name='registro'),

    path('recuperar-clave/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('recuperar-clave/enviado/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('recuperar-clave/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('recuperar-clave/completado/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]