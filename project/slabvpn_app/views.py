from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated

from .forms import LookupForm, RegisterForm
from .models import City, Country, Server
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Provider, InIp, OutIp
from .serializers import InIpSerializer, OutIpSerializer


class ProviderCountriesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, months=3):
        data = Server.get_number_of_countries_per_provider(months)
        if not data:
            return Response({'error': 'No data found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data, status=status.HTTP_200_OK)


class ProviderServersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, months=3):
        data = Server.get_servers_per_provider(months)
        if not data:
            return Response({'error': 'No data found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data, status=status.HTTP_200_OK)


class InIpFilteredView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ip_address = request.query_params.get('ip', None)
        date_since = request.query_params.get('date_since', None)
        if not ip_address or not date_since:
            return Response({'error': 'ip and date_since parameters are required'}, status=status.HTTP_400_BAD_REQUEST)

        records = InIp.get_filtered_records(ip_address, date_since)
        serializer = InIpSerializer(records, many=True)
        if not serializer.data:
            return Response({'error': 'No data found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OutIpFilteredView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ip_address = request.query_params.get('ip', None)
        date_since = request.query_params.get('date_since', None)
        if not ip_address or not date_since:
            return Response({'error': 'ip and date_since parameters are required'}, status=status.HTTP_400_BAD_REQUEST)

        records = OutIp.get_filtered_records(ip_address, date_since)
        serializer = OutIpSerializer(records, many=True)
        if not serializer.data:
            return Response({'error': 'No data found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)

def extract_ip_details(ip_instance):
    if not ip_instance:
        return None, None, None, None, None, None

    provider = ip_instance.server.provider.name
    location = ip_instance.server.location
    if isinstance(location, City):
        country = location.country.name
        city = location.name
    elif isinstance(location, Country):
        country = location.name
        city = None
    else:
        country = None
        city = None

    server_name = ip_instance.server.name
    created_at = ip_instance.created_at

    return provider, country, city, server_name, created_at

@login_required(login_url='/login/')
def index(request):
    if request.method == "POST":
        vpn_status, provider, country, city, server, created_at, is_outbound, date_since, total_count = (
            None, None, None, None, None, None, None, None, 0
        )
        inbound_ips, outbound_ips = [], []

        form = LookupForm(request.POST)
        if form.is_valid():
            ip_address = form.cleaned_data["ip_addr"]
            date_since = form.cleaned_data["datetime"]

            outbound_ips = list(OutIp.get_filtered_records(ip_address, date_since))
            inbound_ips = list(InIp.get_filtered_records(ip_address, date_since))

            latest_out_ip = outbound_ips[0] if outbound_ips else None
            latest_in_ip = inbound_ips[0] if inbound_ips else None

            total_count = len(outbound_ips) + len(inbound_ips)

            if latest_out_ip or latest_in_ip:
                vpn_status = True
                if latest_out_ip:
                    provider, country, city, server, created_at = extract_ip_details(latest_out_ip)
                    is_outbound = True
                elif latest_in_ip:
                    provider, country, city, server, created_at = extract_ip_details(latest_in_ip)
                    is_outbound = False
            else:
                vpn_status = False

        return render(request, "index.html", {
            "form": form,
            "provider": provider,
            "country": country,
            "city": city,
            "vpn_status": vpn_status,
            "server": server,
            "created_at": created_at,
            "is_outbound": is_outbound,
            "date_since": date_since,
            "total_count": total_count,
            "inbound_ips": inbound_ips,
            "outbound_ips": outbound_ips,
        })

    else:
        # Logic for GET requests
        form = LookupForm()
        total_entries = OutIp.get_total_entries()

        countries_per_provider = list(Server.get_number_of_countries_per_provider())
        providers_countries = [entry['provider__name'] for entry in countries_per_provider]
        country_counts_per_provider = [entry['country_count'] for entry in countries_per_provider]

        servers_per_provider = list(Server.get_servers_per_provider())
        servers_providers = [entry['provider__name'] for entry in servers_per_provider]
        server_counts_per_provider = [entry['server_count'] for entry in servers_per_provider]

        entries_per_3_month = list(OutIp.get_entries_per_month(3))
        months = [entry['month'].strftime('%B %Y') for entry in entries_per_3_month]
        entries_count_per_3m = [entry['count'] for entry in entries_per_3_month]

        return render(request, "index.html", {
            "form": form,
            "providers_countries": json.dumps(providers_countries),
            "country_counts_per_provider": json.dumps(country_counts_per_provider),
            "months": json.dumps(months),
            "entries_count_per_3m": json.dumps(entries_count_per_3m),
            "providers_servers": json.dumps(servers_providers),
            "server_counts_per_provider": json.dumps(server_counts_per_provider),
            "total_entries": total_entries,
        })

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def health_check(request):
    return JsonResponse({"status": "ok"})
