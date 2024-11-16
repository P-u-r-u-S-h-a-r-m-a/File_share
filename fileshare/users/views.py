from django.shortcuts import render

from django.shortcuts import render
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SignupSerializer,LoginSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import get_user_model,authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
User = get_user_model()

class GetCSRFTokenView(APIView):
    permission_classes = [AllowAny]  # Change this if you want to restrict access

    def get(self, request):
        csrf_token = get_token(request)
        return Response({'csrfToken': csrf_token})




class SignupView(APIView):
    authentication_classes=[SessionAuthentication]
    permission_classes=[AllowAny]

    def post(self,request): 
        serializer=SignupSerializer(data=request.data)

        if serializer.is_valid():
            user=User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            user_type=serializer.validated_data['user_type']
            )
            return Response({'message': 'User Created Successfully'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    authentication_classes=[SessionAuthentication]
    permission_classes=[AllowAny]
    
    def post(self,request):
        serializer=LoginSerializer(data=request.data)

        if serializer.is_valid():
            validated_data=serializer.validated_data
            user=validated_data.get('user')
            login(request,user)
            return Response({'message':'User logged in successfully'},
                            status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        logout(request)
        return Response({'message':'Logged out Successfully'},
                        status=status.HTTP_200_OK)