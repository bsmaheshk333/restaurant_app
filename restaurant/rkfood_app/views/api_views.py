from rest_framework.views import APIView, Response, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rkfood_app.serializers import (LoginUserSerializer,
                                    RegisterUserSerializer,
                                    CustomerSerializer)
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rkfood_app.models import Customer


class LoginApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': f"you're not authenticated to access this page"},
                            status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_active:
            return Response({"detail": "No active account found with the given credentials"},
                            status=status.HTTP_403_FORBIDDEN)
        return Response({'error': 'method not allowed'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        username: str = request.data.get('username', None).strip()
        password: str = request.data.get('password', None).strip()
        print(f"{username = } and {password = }")
        if not username or not password:
            return Response({'msg': 'invalid username or password'}, status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        print(f"{user = }")
        if user:
            return Response({"msg": f'login success {user.id}'}, status=status.HTTP_200_OK)
        return Response({'msg': 'login failed due to bad request'},status=status.HTTP_400_BAD_REQUEST)



class RegisterApiView(APIView):
    def get(self, request):
        # added permission token here.
        # role based authentication
        if request.user.is_staff:
            # serializers = RegisterUserSerializer(instance=User)
            # only staff is given access to see the user details
            users = User.objects.all().values('username', 'email', 'password')
            return Response({'user': list(users)}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'permission denied'}, status=status.HTTP_403_FORBIDDEN)
        # return Response({'error': 'method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        if not request.user.is_staff:
            return Response({'auth_err': 'access restricted'}, status.HTTP_403_FORBIDDEN)
        username: str = request.data.get('username', None)
        password: str = request.data.get('password', None)
        email = request.data.get('email', None)
        phone: str = request.data.get('phone', None)
        errors = {}
        # validate username
        if username in ['admin', 'root', 'superuser']:
            errors['username'] = f'username {username} is restricted'
        is_username_exist = User.objects.filter(username=username).exists()
        if is_username_exist:
            errors['username_exist'] = (f'this username {username} exist already Please try with '
                                        f'different name.')
        # validate password
        if len(password) < 8 or not any(char.isdigit() for char in password):
            errors['password'] = ("password criteria not met.\n"
                                  "1. password must contain at least one digit/numeric"
                                  "2. password must be 8 characters long")
        # validate email
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = "ERROR! invalid email address."

        if len(phone) != 10:
            errors['phone'] = "please check if phone has exactly 10 digits and contains only numbers"
        elif Customer.objects.filter(phone=phone).exists():
            errors['phone'] = "this number exist already."
        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            Customer.objects.create(user=user, phone=phone)
        except:
            pass
        return Response({'register': 'user registered successfully'}, status=status.HTTP_201_CREATED)
