from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from .models import EmailVerifToken
from datetime import datetime, timedelta
import secrets
from django.core.mail import send_mail
from pinfluence.settings import DEFAULT_FROM_EMAIL, DEFAULT_SERVICE_URL



@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        token_length = 64
        token = secrets.token_hex(token_length)
        
        verification_token = EmailVerifToken.objects.create(user=user, token=token)
        
        verification_link = f"{DEFAULT_SERVICE_URL}/accounts/verify-email/?token={token}"
        
        email_subject = "Please verify your email address"
        email_message = f"Hello {user.username},\n\nPlease click on the following link to verify your email address:\n{verification_link}"
        
        send_mail(email_subject, email_message, DEFAULT_FROM_EMAIL, [user.email])

        return Response({"detail": "Please check your email for verification."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request):
    token = request.query_params.get('token')
    if token:
        try:
            verification_token = EmailVerifToken.objects.get(token=token)
            user = verification_token.user
            user.is_active = True
            user.save()
            verification_token.delete()
            return Response({"detail": "Email verified successfully."}, status=status.HTTP_200_OK)
        except EmailVerifToken.DoesNotExist:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Token parameter is missing."}, status=status.HTTP_400_BAD_REQUEST)




# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])

# def test_token(request):
#     return Response("passed for {}".format(request.user.email))