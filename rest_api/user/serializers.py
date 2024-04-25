from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserAnswer

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'is_staff']
        
    def validate(self, data):
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError("Email is already registered.")
        return data
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer