# Create your views here.
from rest_framework import generics
from core.models import User
from core.serializers import UserSerializer


class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
