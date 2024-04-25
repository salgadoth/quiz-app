from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField 
from ..quiz.models import Question, Choice

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    submited_choice = models.ManyToManyField(Choice, blank=True)
    submited_words = ArrayField((models.CharField(max_length=50, blank=True, null=True)))
    submited_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s answer to {self.question.text}"