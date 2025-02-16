from django.contrib.auth import get_user_model


from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import RegisterSerializer as r, RegisterSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
