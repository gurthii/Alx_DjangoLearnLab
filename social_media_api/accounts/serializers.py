# accounts/serializers.py

from rest_framework import serializers
# [1] REQUIRED IMPORT
from rest_framework.authtoken.models import Token 
from django.contrib.auth import get_user_model
from .models import CustomUser

# --- Registration Serializer ---
class UserRegistrationSerializer(serializers.ModelSerializer):
    # [2] REQUIRED FIELD DEFINITION
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    # Field to return the token upon successful creation
    token = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'token')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # [4] REQUIRED USER CREATION LOGIC
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # [3] REQUIRED TOKEN CREATION LOGIC
        token = Token.objects.create(user=user)
        
        # Add the token key to the user instance before returning
        user.token = token.key

        return user


# --- User Profile Serializer (Remains mostly the same) ---
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'bio', 'profile_picture', 'followers', 'following')
        read_only_fields = ('username', 'email', 'followers', 'following')