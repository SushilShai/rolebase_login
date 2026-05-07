from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
import re

class LoginView(APIView):
    permission_classes = []  # AllowAny

    def post(self, request):
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")

        if not phone_number or not password:
            return Response({"error": "Phone number and password required"}, status=status.HTTP_400_BAD_REQUEST)

        # Regex validation
        if not re.match(r'^(97|98)\d{8}$', phone_number):
            return Response({"error": "Phone number must be 10 digits starting with 97 or 98"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile = UserProfile.objects.get(phone_number=phone_number)
            user = profile.user
        except UserProfile.DoesNotExist:
            return Response({"error": "Invalid phone number or password"}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=user.username, password=password)
        if user is None or not user.is_active:
            return Response({"error": "Invalid credentials or inactive account"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "user_id": user.id,
            "name": user.get_full_name() or user.username,
            "role": profile.role,
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        }, status=status.HTTP_200_OK)
