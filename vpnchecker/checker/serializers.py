from rest_framework import serializers
from .models import Provider, Server, InIp, OutIp, City, Country

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['id', 'name', 'created_at', 'updated_at']

class ServerSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer()
    city_name = serializers.SerializerMethodField()
    country_name = serializers.SerializerMethodField()

    class Meta:
        model = Server
        fields = ['id', 'name', 'provider', 'location_type', 'city_name', 'country_name', 'created_at', 'updated_at']

    def get_city_name(self, obj):
        if obj.location_type == 'City':
            city = City.objects.filter(id=obj.location_id).first()
            return city.name if city else None
        return None

    def get_country_name(self, obj):
        if obj.location_type == 'City':
            city = City.objects.filter(id=obj.location_id).select_related('country').first()
            return city.country.name if city and city.country else None
        elif obj.location_type == 'Country':
            country = Country.objects.filter(id=obj.location_id).first()
            return country.name if country else None
        return None

class InIpSerializer(serializers.ModelSerializer):
    server = ServerSerializer()

    class Meta:
        model = InIp
        fields = ['id', 'ip', 'server', 'created_at', 'updated_at']

class OutIpSerializer(serializers.ModelSerializer):
    server = ServerSerializer()

    class Meta:
        model = OutIp
        fields = ['id', 'ip', 'server', 'created_at', 'updated_at']