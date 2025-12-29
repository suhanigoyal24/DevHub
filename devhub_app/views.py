from django.shortcuts import render
# devhub_app/views.py
# Create your views here.
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from rest_framework import generics, permissions
from .models import Repository
from .serializers import RepositorySerializer
import os
from django.conf import settings
from django.http import JsonResponse

User = get_user_model()

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        user = User.objects.create_user(
            username=request.data["username"],
            email=request.data["email"],
            password=request.data["password"]
        )
        token = RefreshToken.for_user(user)
        return Response({
            "access": str(token.access_token),
            "user_id": user.id
        })


class LoginView(generics.GenericAPIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=400)

        token = RefreshToken.for_user(user)
        return Response({
            "access": str(token.access_token),
            "user_id": user.id
        })


def home(request):
    return JsonResponse({"message": "Welcome to DevHub API"})

APNAGIT_DIR = os.path.join(settings.BASE_DIR, ".apnaGit/repos")

class RepositoryListCreateView(generics.ListCreateAPIView):
    serializer_class = RepositorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # List only repos owned by logged-in user
        return Repository.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Save the repository with the current user as owner
        repo = serializer.save(owner=self.request.user)

        # Create a folder for this repo inside .apnaGit
        repo_path = os.path.join(APNAGIT_DIR, str(repo.id))
        os.makedirs(repo_path, exist_ok=True)