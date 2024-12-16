from rest_framework import serializers
from .models import Provider, Server, InIp, OutIp

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['id', 'name', 'created_at', 'updated_at']

class ServerSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer()

    class Meta:
        model = Server
        fields = ['id', 'name', 'provider', 'location_type', 'location_id', 'created_at', 'updated_at']

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
