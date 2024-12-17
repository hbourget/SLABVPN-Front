from django.db import models
from django.db.models import Count, Subquery, OuterRef, Q, Case, When, F
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
from datetime import timedelta
import uuid

class Provider(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(unique=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        #managed = False
        db_table = 'providers'


class Server(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='servers')

    # Custom polymorphic fields
    location_type = models.CharField(max_length=50, choices=[('City', 'City location'), ('Country', 'Country location')])
    location_id = models.UUIDField()

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    @property
    def location(self):
        if self.location_type == 'City':
            return City.objects.filter(id=self.location_id).first()
        elif self.location_type == 'Country':
            return Country.objects.filter(id=self.location_id).first()
        return None

    @classmethod
    def get_servers_per_provider(cls, months=3):
        time_period = now() - timedelta(days=months * 30)

        return (
            cls.objects
            .filter(created_at__gte=time_period)
            .values('provider__id', 'provider__name')
            .annotate(server_count=Count('id'))
            .order_by('-server_count')
        )

    @classmethod
    def get_number_of_countries_per_provider(cls, months=3):
        time_period = now() - timedelta(days=months * 30)

        # Subquery to get the country ID when location_type is 'City'
        city_country_subquery = City.objects.filter(
            id=OuterRef('location_id')
        ).values('country__id')[:1]

        return (
            cls.objects
            .filter(created_at__gte=time_period)
            .annotate(
                country_id=Case(
                    When(location_type='Country', then=F('location_id')),  # Direct country reference
                    When(location_type='City', then=Subquery(city_country_subquery)),  # Resolve country via city
                    default=None,
                    output_field=models.UUIDField()
                )
            )
            .values('provider__id', 'provider__name')
            .annotate(
                unique_countries=Count('country_id', distinct=True)  # Count unique countries
            )
            .order_by('-unique_countries')
        )

    def __str__(self):
        return self.name

    class Meta:
        #managed = False
        db_table = 'servers'


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(unique=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        #managed = False
        db_table = 'countries'


class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        #managed = False
        db_table = 'cities'


class InIp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip = models.TextField()
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='in_ips')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.ip

    class Meta:
        #managed = False
        db_table = 'in_ips'

    @classmethod
    def get_filtered_records(cls, ip_address, date_since):
        return cls.objects.filter(
            ip=ip_address,
            updated_at__gte=date_since
        ).select_related('server__provider').order_by('-created_at')


class OutIp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip = models.TextField()
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='out_ips')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.ip

    class Meta:
        #managed = False
        db_table = 'out_ips'

    @classmethod
    def get_filtered_records(cls, ip_address, date_since):
        return cls.objects.filter(
            ip=ip_address,
            updated_at__gte=date_since
        ).select_related('server__provider').order_by('-created_at')

    @classmethod
    def get_total_entries(cls):
        return cls.objects.count()

    @classmethod
    def get_entries_per_month(cls, months=3):
        today = now()
        six_months_ago = today - timedelta(days=months * 30)
        return (
            cls.objects.filter(created_at__gte=six_months_ago)
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )