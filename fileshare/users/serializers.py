from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['username','email','password','user_type']

    def create(self,validated_data):
        user=User.objects.create_user(
         username=validated_data['username'],
         email=validated_data['email'],
         password=validated_data['password'],
         user_type=validated_data['user_type']       
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)

    def validate(self,data):
        username=data.get("username")
        password=data.get("password")

        if username and password:
            user=authenticate(username=username,password=password)
            if user is None:
                raise serializers.ValidationError("Invalid Credentials")
        else:
            raise serializers.ValidationError("Please give both username and password")
        
        data['user'] = user 
        return data