from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CategorySerializer, QuizSerializer, QuestionSerializer, ChoiceSerializer
from .models import Category, Question, Quiz

# Create your views here.
class CategoryListView(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, _):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailView(generics.RetrieveAPIView):
    def get(request, *args, **kwargs):
        title = kwargs['title']
        category = Category.objects.filter(title__icontains=title).first()
        if not category:
            return Response({'message': 'Category not found'}, status=status.HTTP_400_BAD_REQUEST) 
        data = Quiz.objects.filter(category=category.id)
        if not data.first():
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = QuizSerializer(data, many = True)
        return Response(serializer.data)
        
class QuizListView(APIView):
    def post(self, request):
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuizListByCategoryView(generics.ListAPIView):
    def get(request, *args, **kwargs):
        title = kwargs['title']
        category = Category.objects.filter(title__icontains=title).first()
        if not category:
            return Response({'message': 'Category not found'}, status=status.HTTP_400_BAD_REQUEST) 
        data = Quiz.objects.filter(category=category.id)
        serializer = QuizSerializer(data, many = True)
        return Response(serializer.data)
    

class QuestionListView(APIView):
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            serializer = QuestionSerializer(question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, _):
        return Question.objects.all()
    
class QuestionListByQuizView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    
    def get_queryset(self):
        quiz_id = self.kwargs['pk']
        return Question.objects.filter(quiz=quiz_id)

class ChoiceListView(APIView):
    def post(self, request):
        serializer = ChoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)