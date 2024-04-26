from rest_framework import status
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