from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import CustomUser
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.utils.http import http_date
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    def post(self, request):
        try:
            user = CustomUser.objects.get(email=request.data['email'])
        except CustomUser.DoesNotExist:
            return Response({"message": "Usuario no encontrado"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(request.data['password']):
            return Response({"message": "Usuario o contraseña incorrectos"}, status=status.HTTP_400_BAD_REQUEST)

        # Generar el JWT (Refresh Token y Access Token)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        serializer = UserSerializer(instance=user)

        # Configurar la cookie del token (si deseas usar cookies)
        max_age = 3600  # Duración de 1 hora
        expires_datetime = datetime.utcnow() + timedelta(seconds=max_age)  # Fecha de expiración (1 hora después)
        expires_timestamp = expires_datetime.timestamp()  # Convertir a timestamp
        expires_http = http_date(expires_timestamp) # Convertir a formato HTTP  
        response = Response({"user": serializer.data, "token": access_token}, status=status.HTTP_200_OK)

        # Configurar la cookie del JWT (si se desea almacenar en cookies)
        response.set_cookie(
            key="Token",  
            value=access_token,  
            max_age=max_age,     
            expires=expires_http,  
            httponly=True,          
            secure=False,        
            samesite="Lax"         
        )
        return response

class RegisterView(APIView):
    def post(self, request):
        user = CustomUser.objects.filter(username=request.data['username'])

        if user:
            return Response({"message": "El usuario ya existe"}, status=status.HTTP_400_BAD_REQUEST)
        elif CustomUser.objects.filter(email=request.data['email']):
            return Response({"message": "El email ya existe"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            user = CustomUser.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            serializer = UserSerializer(instance=user)
            
            # Configurar la expiración de las cookies
            max_age = 3600  # 1 semana en segundos
            expires_datetime = datetime.utcnow() + timedelta(seconds=max_age)  # Objeto datetime
            expires_timestamp = expires_datetime.timestamp()
            expires_http = http_date(expires_timestamp)
            # Crear una respuesta
            response = Response({"user": serializer.data, "token": access_token}, status=status.HTTP_201_CREATED)
            
            # Configurar la cookie del token
            response.set_cookie(
                key="Token",  
                value=access_token,  
                max_age=max_age,     
                expires=expires_http,  
                httponly=True,          
                secure=False,        
                samesite="Lax"         
            )
            
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        token = request.COOKIES.get("Token")
        if token:
            try:
                token_obj = Token.objects.get(key=token)
                token_obj.delete()  # Eliminar el token
            except Token.DoesNotExist:
                pass
        response = Response({"message": "Sesión cerrada correctamente"})
        response.delete_cookie("Token")  # Eliminar cookie
        return response
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ProfileView(APIView):
    def get(self, request):
        user = request.user
        return Response({"username": user, "message": "Profile successful"})
