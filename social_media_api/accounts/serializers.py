# accounts/serializers.py

from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        # We only need username, email, and password for registration
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        # Hash the password before saving
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # Exclude password for profile display
        fields = ('username', 'email', 'bio', 'profile_picture', 'followers', 'following')
        # Allow updating bio and profile picture
        read_only_fields = ('username', 'email', 'followers', 'following')