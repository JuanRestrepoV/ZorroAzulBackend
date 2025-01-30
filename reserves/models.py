from django.db import models
from events.models import *
from users.models import CustomUser
# Create your models here.

class ReserveStatus(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'reserve_status'
        
class Reserves(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_event = models.ForeignKey('events.Events', models.DO_NOTHING, db_column='id_event', blank=True, null=True)
    rangehour = models.CharField(db_column='RangeHour', blank=True, null=True)  # Field name made lowercase.
    capacity = models.IntegerField(blank=True, null=True)
    id_floor = models.ForeignKey('events.Floor', models.DO_NOTHING, db_column='id_floor', blank=True, null=True)
    table = models.CharField(blank=True, null=True)
    user = models.ForeignKey('users.CustomUser', models.DO_NOTHING, db_column='user_id', blank=True, null=True)
    id_reserve_status = models.ForeignKey('ReserveStatus', models.DO_NOTHING, db_column='id_reserve_status', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'reserves'

class ReserveAdditionalServices(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_service = models.ForeignKey('events.Services', models.DO_NOTHING, db_column='id_service')
    id_reserve = models.ForeignKey('Reserves', models.DO_NOTHING, db_column='id_reserve')

    class Meta:
        managed = False
        db_table = 'reserve_additional_services'