from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserAnswer
from ..quiz.serializers import ChoiceSerializer
from ..quiz.models import Choice, Quiz

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
    submited_choice = serializers.PrimaryKeyRelatedField(queryset=Choice.objects.all(), many=True, required=False)
    submited_words = serializers.ListField(child=serializers.CharField(max_length=50), allow_null=True, default=[])
    
    class Meta:
        model = UserAnswer
        fields = ['id', 'user', 'question', 'submited_choice', 'submited_words']
        
    def create(self, validated_data):
        submited_choice_data = validated_data.pop('submited_choice')
        submited_words_data = validated_data.pop('submited_words')
        user_answer = UserAnswer.objects.create(**validated_data)

        # Add submitted choices to the user answer
        for choice_data in submited_choice_data:
            choice = Choice.objects.get(id=choice_data.id)
            user_answer.submited_choice.add(choice)

        # Set submitted words for the user answer
        user_answer.submited_words = submited_words_data
        user_answer.save()

        return user_answer
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['is_staff'] = user.is_staff

        return token