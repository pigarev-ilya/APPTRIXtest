from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from backend.custom_filter_distace_user import CustomDistanceFilter
from backend.models import User
from backend.serializers import RegistrationSerializer, CustomAuthTokenSerializer, ListUserSerializer
from backend.signals import liked_user_signal


class RegisterView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            data = {}
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                token = Token.objects.get_or_create(user=user)[0].key
                data["message"] = 'User registered successfully'
                data["email"] = user.email
                data["token"] = token
                return JsonResponse({'Status': True, 'Data': data})
            else:
                return JsonResponse({'Status': False, 'Errors': serializer.errors})
        except IntegrityError as error:
            return JsonResponse({'Status': False, 'Errors': f'{str(error)}'})
        except KeyError as error:
            return JsonResponse({'Status': False, 'Errors': f'Field {str(error)} missing.'})


class LoginView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer


class UserLikesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, liked_user_id, *args, **kwargs):
        queryset_all_users = User.objects.all()
        likes_current_user = queryset_all_users.filter(likes_from=request.user).values_list('id', flat=True)
        if liked_user_id in likes_current_user:
            return JsonResponse({'Status': False, 'Errors': 'Like already sent.'})
        if request.user.id == liked_user_id:
            return JsonResponse({'Status': False, 'Errors': "You can't send Like to yourself."})
        liked_user = queryset_all_users.filter(id=liked_user_id).first()
        if not liked_user:
            return JsonResponse({'Status': False, 'Errors': f'User is not found.'})
        liked_user.likes_from.add(request.user)
        user_liked_in_response = queryset_all_users.filter(user_like=request.user, email=liked_user.email)
        if user_liked_in_response:
            liked_user_signal.send(sender=self.__class__, emails=[request.user.email, liked_user.email],
                                   names=[request.user.first_name, liked_user.first_name])
            return JsonResponse({'Status': True, 'Message': f'Like sent. '
                                                            f'There is a match, email {liked_user.email}'})
        return JsonResponse({'Status': True, 'Message': f'Like sent.'})


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = ListUserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, CustomDistanceFilter]
    filterset_fields = ['first_name', 'last_name', 'gender']

    def get_queryset(self):
        return User.objects.all().exclude(Q(id=self.request.user.id) | Q(is_superuser=True))
