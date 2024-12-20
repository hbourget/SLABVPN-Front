from django.urls import path
from .views import ProviderCountriesView, ProviderServersView, InIpFilteredView, OutIpFilteredView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('api/providers/countries/', ProviderCountriesView.as_view(), name='provider-countries'),
    path('api/providers/servers/', ProviderServersView.as_view(), name='provider-servers'),
    path('api/in_ips/', InIpFilteredView.as_view(), name='in-ip-filtered'),
    path('api/out_ips/', OutIpFilteredView.as_view(), name='out-ip-filtered'),
]