from rest_framework import serializers
from .models import Category, Quiz, Question, Choice

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields= ('id', 'title')
        
    def validate(self, data):
        if Category.objects.filter(title=data.get('title')).exists():
            raise serializers.ValidationError("Category with this name already exists.")
        return data
            
        
class QuizSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField()
    
    class Meta:
        model = Quiz
        fields = ('id', 'category', 'category_id', 'title', 'created_date')
        
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct', 'created_date']

class QuestionSerializer(serializers.ModelSerializer):
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())  # Assuming Quiz is the related model
    choices = ChoiceSerializer(source='related_questions', many=True, required=False)  # Nested serialization for choices

    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        choices_data = validated_data.pop('related_questions')
        question = Question.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)
        return question