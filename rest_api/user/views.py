from collections import defaultdict
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
    user_answers = UserAnswer.objects.filter(user=request.user).select_related('question').prefetch_related('submited_choice')

    # Dictionary to store percentage correct for each quiz
    quiz_percentages = defaultdict(int)
    quiz_total_questions = defaultdict(int)
    quiz_correct_answers = defaultdict(int)

    # Iterate over each UserAnswer instance
    for user_answer in user_answers:
        quiz_id = user_answer.question.quiz.id
        quiz_total_questions[quiz_id] += 1

        # Check if the submitted choices are correct
        if user_answer.submited_choice.filter(is_correct=True).exists():
            quiz_correct_answers[quiz_id] += 1

    # Calculate the percentage for each quiz
    for quiz_id, total_questions in quiz_total_questions.items():
        correct_answers = quiz_correct_answers[quiz_id]
        if total_questions > 0:
            quiz_percentages[quiz_id] = (correct_answers / total_questions) * 100
        else:
            quiz_percentages[quiz_id] = 0

    return Response(dict(quiz_percentages))