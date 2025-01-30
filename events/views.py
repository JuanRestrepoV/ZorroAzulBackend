from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *

# Create your views here.
class EventsView(APIView):
    def get(self, request):
        events = Events.objects.all().select_related(
            'id_type_event'
        ).prefetch_related(
            'eventsservices_set',
            'eventsservices_set__id_service',
            'eventsservices_set__id_service__service_type',
        )
        serializer = EventsSerializer(events, many=True)
        return Response(serializer.data)
    
class AditionalServicesView(APIView):
    def get(self, request):
        services = Services.objects.filter(service_type_id=2).select_related(
            'service_type'
        )
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

class FloorView(APIView):
    def get(self, request):
        floors = Floor.objects.all()
        serializer = FloorSerializer(floors, many=True)
        return Response(serializer.data)