from django.shortcuts import render
from .forms import LookupForm
from .models import OutIp, InIp, City, Country, Provider
import json

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

        countries_per_provider = list(Provider.get_countries_per_provider())
        providers_countries = [entry['name'] for entry in countries_per_provider]
        country_counts_per_provider = [entry['country_count'] for entry in countries_per_provider]

        servers_per_provider = list(Provider.get_servers_per_provider())
        servers_providers = [entry['name'] for entry in servers_per_provider]
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
