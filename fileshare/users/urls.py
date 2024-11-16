from django.urls import path
from .views import *



urlpatterns = [
    path('get-csrf-token/', GetCSRFTokenView.as_view(), name='get-csrf-token'),
    path("signup/",SignupView.as_view(),name='signup'),
    path("login/",LoginView.as_view(),name='login'),
    path("logout/",LogoutView.as_view(),name='logout'),
]