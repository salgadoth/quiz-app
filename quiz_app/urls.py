"""
URL configuration for quiz_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_api.quiz.views import CategoryListView, CategoryDetailView, QuizListView, QuestionListView, QuizListByCategoryView, QuestionListByQuizView, ChoiceListView
from rest_api.user.views import UserRegisterView, UserListView, UserLoginView, UserAnswerView, get_user_answers, calculate_completion_percentage

prefix = 'api'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{prefix}/category/', CategoryListView.as_view(), name="category"),
    path(f'{prefix}/category/<str:title>', CategoryDetailView.as_view(), name='category_detail'),
    path(f'{prefix}/category/<str:title>/quizzes', QuizListByCategoryView.as_view(), name='quiz_detail'),
    path(f'{prefix}/quiz/', QuizListView.as_view(), name='quiz'),
    path(f'{prefix}/quiz/<int:pk>/questions', QuestionListByQuizView.as_view(), name='question_detail'),
    path(f'{prefix}/question/', QuestionListView.as_view(), name='question'),
    path(f'{prefix}/answer/', UserAnswerView.as_view(), name='answer'),
    path(f'{prefix}/user/', UserListView.as_view(), name="user_detail"),
    path(f'{prefix}/user/total-answers', get_user_answers, name="user_total_answers"),
    path(f'{prefix}/user/prct-answers', calculate_completion_percentage, name="user_percentage_answers"),
    path(f'{prefix}/auth/register/', UserRegisterView.as_view(), name='user_register'),
    path(f'{prefix}/auth/login/', TokenObtainPairView.as_view(), name='obtain_token'),
    path(f'{prefix}/auth/refresh/', TokenRefreshView.as_view(), name='refresh_token')
]
