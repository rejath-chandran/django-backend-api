from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from .serializers import RegisterSerializer, UserSerializer, EmailTokenObtainPairSerializer
from .utils import clear_refresh_cookie, set_refresh_cookie, REFRESH_COOKIE_NAME



User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # refresh = RefreshToken.for_user(user)
        # access = refresh.access_token

        response = Response(
            {
                "user": UserSerializer(user).data,
                # "access": str(access),      # 🔥 send ACCESS TOKEN in body
                "detail": "Registration successful",
            },
            status=status.HTTP_201_CREATED,
        )

        # Store ONLY refresh token in cookie (HttpOnly)
        # set_refresh_cookie(response, str(refresh))
        return response



class LoginView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        access = response.data.get("access")
        refresh = response.data.get("refresh")

        if not access or not refresh:
            return Response({"detail": "Invalid login"}, status=400)

        # Prepare clean response
        user = User.objects.get(email=request.data.get("email"))
        new_response = Response(
            {
                "user": UserSerializer(user).data,
                "access": access,     # 🔥 send ACCESS TOKEN in body
                "detail": "Login successful",
            },
            status=200,
        )

        # Store ONLY refresh token in HttpOnly cookie
        set_refresh_cookie(new_response, refresh)
        return new_response


class CookieTokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_cookie = request.COOKIES.get(REFRESH_COOKIE_NAME)

        if not refresh_cookie:
            return Response(
                {"detail": "No refresh token cookie found"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = self.get_serializer(data={"refresh": refresh_cookie})
        serializer.is_valid(raise_exception=True)

        new_access = serializer.validated_data["access"]

        response = Response(
            {
                "access": new_access,      # 🔥 send ACCESS TOKEN in body
                "detail": "Token refreshed",
            },
            status=status.HTTP_200_OK,
        )

        # Keep same refresh token cookie, do NOT rotate
        return response


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_cookie = request.COOKIES.get(REFRESH_COOKIE_NAME)

        if refresh_cookie:
            try:
                token = RefreshToken(refresh_cookie)
                token.blacklist()
            except Exception:
                pass

        response = Response({"detail": "Logged out"}, status=200)
        clear_refresh_cookie(response)
        return response



class ProtectedView(APIView):
    """
    GET /api/protected/
    - Requires valid access token (from Authorization header or cookie depending on client)
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_data = UserSerializer(request.user).data
        return Response(
            {"message": "You are authenticated", "user": user_data},
            status=status.HTTP_200_OK,
        )
