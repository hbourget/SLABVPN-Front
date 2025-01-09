from django.contrib.auth.views import LogoutView
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ProviderCountriesView, ProviderServersView, InIpFilteredView, OutIpFilteredView, login_view, \
    register_view, health_check

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/providers/countries/', ProviderCountriesView.as_view(), name='provider-countries'),
    path('api/providers/servers/', ProviderServersView.as_view(), name='provider-servers'),
    path('api/in_ips/', InIpFilteredView.as_view(), name='in-ip-filtered'),
    path('api/out_ips/', OutIpFilteredView.as_view(), name='out-ip-filtered'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("health/", health_check, name="health_check"),
]