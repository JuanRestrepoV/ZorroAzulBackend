from rest_framework import serializers
from .models import *
from events.serializers import *
from events.serializers import *
from users.serializers import *

class ReserveStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReserveStatus
        fields = '__all__'

class ReserveAdditionalServicesSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = ReserveAdditionalServices
        fields = '__all__'
        
class ReserveAdditionalServicesSerializer(serializers.ModelSerializer):
    id_service = ServiceSerializer(many=False)
    class Meta:
        model = ReserveAdditionalServices
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        return representation['id_service']['name']
        
class ReserveSerializer(serializers.ModelSerializer):
    id_event = EventsSerializer()
    user = UserSerializer()
    id_floor = FloorSerializer()
    id_reserve_status = ReserveStatusSerializer()
    reserveadditionalservices_set = ReserveAdditionalServicesSerializer(many=True)
    class Meta:
        model = Reserves
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
    
        data = {
            'id': representation['id'],
            'event_name': representation['id_event']['title'],
            'type_event': representation['id_event']['type_event'],
            'event_services': [ service['name'] for service in representation['id_event']['services'] ] + [ service for service in representation['reserveadditionalservices_set'] ],
            'rangehour': representation['rangehour'],
            'capacity': representation['capacity'],
            'floor_name': representation['id_floor']['name'],
            'table': representation['table'],
            'user': representation['user']['username'],
            'id_reserve_status': representation['id_reserve_status']['name'],
            'created_at': representation['created_at'],
            'updated_at': representation['updated_at'],
        }
        
        return data
class ReserveSerializerCreate(serializers.ModelSerializer):    
    class Meta:
        model = Reserves
        fields = '__all__'

class ReserveAdditionalServicesSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = ReserveAdditionalServices
        fields = '__all__'
        
class ReserveAdditionalServicesSerializer(serializers.ModelSerializer):
    id_service = ServiceSerializer(many=False)
    class Meta:
        model = ReserveAdditionalServices
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        data = {
            'id': representation['id'],
            'id_service': representation['id_service']['name'],
            'id_reserve': representation['id_reserve']['id'],
        }
        
        return data