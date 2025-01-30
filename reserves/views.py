from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.db import transaction
from datetime import datetime
# Create your views here.

class ReservesView(APIView):
    def get(self, request):
        estado = ['PENDIENTE', 'EN PROCESO', 'CONFIRMADA', 'CANCELADA']
        # reservas_por_estado = {}
        
        reserves = Reserves.objects.all().select_related(
            'id_event',
            'id_event__id_type_event',
            'id_floor',
            'user',
            'id_reserve_status',
        ).prefetch_related(
            'id_event__eventsservices_set',
            'id_event__eventsservices_set__id_service',
            'id_event__eventsservices_set__id_service__service_type',
            'reserveadditionalservices_set',
            'reserveadditionalservices_set__id_service',
            'reserveadditionalservices_set__id_service__service_type',
            'reserveadditionalservices_set__id_reserve',
        )
        
        reservas_por_estado = { e: ReserveSerializer(Reserves.objects.filter(id_reserve_status__name=e), many=True).data for e in estado }
        
        # serializer = ReserveSerializer(reserves, many=True)
        return Response(reservas_por_estado)
    
    def post(self, request):
        data = request.data
        with transaction.atomic():
            try:
                additional_services = [service['id'] for service in data.get('additional_services', [])]

                new_reserve_data = {
                    'id_event': data['id_event'],
                    'rangehour': data['rangeHour'],
                    'capacity': data['capacity'],
                    'id_floor': data['id_floor'],
                    'table': data['table'],
                    'user': data['user'],
                    'id_reserve_status': data['id_reserve_status'],
                    'created_at': datetime.now(),
                    'updated_at': datetime.now(),
                }

                reserve_serializer = ReserveSerializerCreate(data=new_reserve_data)
                if not reserve_serializer.is_valid():
                    return Response(reserve_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                reserve_instance = reserve_serializer.save()  # Guarda y obtiene el objeto con ID

                # Guardar los servicios adicionales
                for service_id in additional_services:
                    new_additional_service = {
                        'id_service': service_id,
                        'id_reserve': reserve_instance.id,  # Usa el ID del objeto creado
                    }

                    additional_service_serializer = ReserveAdditionalServicesSerializerCreate(data=new_additional_service)
                    if not additional_service_serializer.is_valid():
                        raise ValueError(additional_service_serializer.errors)  # Forzar rollback si hay error

                    additional_service_serializer.save()

                return Response({"message": "Reserva creada correctamente"}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReserveAdditionalServicesView(APIView):
    def get(self, request):
        reserves = ReserveAdditionalServices.objects.all().select_related(
            'id_service',
            'id_reserve',
        )
        serializer = ReserveAdditionalServicesSerializer(reserves, many=True)
        return Response(serializer.data)