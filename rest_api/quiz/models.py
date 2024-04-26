from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta: 
        verbose_name_plural = 'Categories'

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name_plural = 'Quizzes'

class Question(models.Model):
    CHOICE_TYPE = [
        ('SINGLE', 'Single Choice'),
        ('MULTIPLE', 'Multiple Choice'),
        ('WORD', 'Words choice')
    ]
    
    title = models.CharField(max_length=100, default='title')
    text = models.CharField(max_length=255, blank=True, null=True)
    choice_type = models.CharField(max_length=50, choices=CHOICE_TYPE)
    created_date = models.DateTimeField(auto_now_add=True)
    quiz = models.ForeignKey(Quiz, related_name='related_quiz', on_delete=models.CASCADE)
    correct_words = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    
class Choice(models.Model):
    text = models.CharField(max_length=255, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, related_name='related_questions', on_delete=models.CASCADE)