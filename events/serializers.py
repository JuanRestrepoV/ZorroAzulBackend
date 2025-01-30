from rest_framework import serializers
from .models import *

class TypeEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeEvent
        fields = '__all__'

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'
        
class ServiceSerializer(serializers.ModelSerializer):
    service_type = ServiceTypeSerializer(many=False)
    class Meta:
        model = Services
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        data = {
            'id': representation['id'],
            'name': representation['name'],
            'service_type': representation['service_type']['name'],
            'image': representation['image']
        }
        
        return data
        
class EventsServicesSerializer(serializers.ModelSerializer):
    id_service = ServiceSerializer(many=False)

    class Meta:
        model = EventsServices
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        return representation['id_service']
        
class EventsSerializer(serializers.ModelSerializer):
    id_type_event = TypeEventSerializer(many=False)
    eventsservices_set = EventsServicesSerializer(many=True)
    class Meta:
        model = Events
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        data = {
            'id': representation['id'],
            'title': representation['title'],
            'type_event': representation['id_type_event']['name'],
            'description': representation['description'],
            'image': representation['image'],
            'price': representation['price'],
            'short_description': representation['short_description'],
            'services': representation['eventsservices_set']
        }
        
        return data
    
class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = '__all__'