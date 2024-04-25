from django.contrib import admin
from .quiz.models import Category, Quiz, Question, Choice
from .user.models import UserAnswer

# Register your models here.
admin.site.register(Category)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(UserAnswer)