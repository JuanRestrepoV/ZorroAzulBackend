from django.db import models

# Create your models here.
class Events(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField(max_length=255, blank=True, null=True)
    id_type_event = models.ForeignKey('TypeEvent', models.DO_NOTHING, db_column='id_type_event', blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    price = models.FloatField()

    class Meta:
        managed = False
        db_table = 'events'
        
class TypeEvent(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'type_event'

class ServiceType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'service_type'
        
class Services(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    service_type = models.ForeignKey('ServiceType', models.DO_NOTHING)
    image = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'services'
        
class EventsServices(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_service = models.ForeignKey('Services', models.DO_NOTHING, db_column='id_service')
    id_event = models.ForeignKey('Events', models.DO_NOTHING, db_column='id_event')

    class Meta:
        managed = False
        db_table = 'events_services'
        
class Floor(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'floor'