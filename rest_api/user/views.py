from collections import defaultdict
from rest_api.quiz.models import Question, Quiz
from rest_api.user.models import UserAnswer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from .serializers import UserAnswerSerializer, UserSerializer

class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={request: request})
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        refresh['is_staff'] = user.is_staff
        refresh['username'] = user.username
        return Response({'token': str(refresh), 'user_id': user.pk}, status=status.HTTP_200_OK)

class UserRegisterView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if(serializer.is_valid()):
            user = serializer.save()
            
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserListView(APIView):
    def get(self, _):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
        
class UserAnswerView(APIView):
    def post(self, request):
        serializer = UserAnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserAnswerCheckView(APIView):
    def get(self, request, question_id):
        user = request.user  # Assuming user is authenticated
        # Check if the user has submitted an answer to the question
        try:
            user_answer = UserAnswer.objects.get(user=user, question_id=question_id)
            serializer = UserAnswerSerializer(user_answer)
            return Response(serializer.data)
        except UserAnswer.DoesNotExist:
            return Response({'message': 'User has not submitted an answer to this question'}, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_answers(request):
    user = request.user  # Assuming user is authenticated
    user_answers = UserAnswer.objects.filter(user=user)
    data = []
    for user_answer in user_answers:
        quiz_id = user_answer.question.quiz.id
        answer_data = {
            'quiz_id': quiz_id,
            'user': user_answer.user.username,
            'question': user_answer.question.title,
            'submited_choice': list(user_answer.submited_choice.values_list('id', flat=True)),
            'submited_words': user_answer.submited_words,
            'submited_at': user_answer.submited_at
        }
        data.append(answer_data)
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def calculate_completion_percentage(request):
    recent_answers = UserAnswer.objects.filter(user=request.user).order_by('-submited_at')[:5]

    # Dictionary to store completion percentage for each quiz
    quiz_percentages = {}

    for user_answer in recent_answers:
        quiz_title = user_answer.question.quiz.title
        quiz_total_questions = Question.objects.filter(quiz=user_answer.question.quiz).count()
        correct_answers = user_answer.submited_choice.filter(is_correct=True).count()

        # Calculate the completion percentage for the quiz
        if quiz_total_questions > 0:
            completion_percentage = (correct_answers / quiz_total_questions) * 100
        else:
            completion_percentage = 0

        # Store the completion percentage in the dictionary
        quiz_percentages[quiz_title] = completion_percentage

    return Response(quiz_percentages)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recent_quiz(request):
    user = request.user  # Assuming user is authenticated
    recent_answers = UserAnswer.objects.filter(user=user).order_by('-submited_at')[:5]
    recent_quizzes_data = []
    for answer in recent_answers:
        quiz_data = {
            'quiz_id': answer.question.quiz.id,
            'quiz_title': answer.question.quiz.title,
            'submited_at': answer.submited_at
        }
        recent_quizzes_data.append(quiz_data)
    
    if recent_quizzes_data:
        return Response(recent_quizzes_data)
    else:
        return Response({'message': 'User has not answered any questions yet.'}, status=status.HTTP_404_NOT_FOUND)
   