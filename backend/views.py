from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from backend.serializers import RegistrationSerializer, CustomAuthTokenSerializer


class RegisterView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            data = {}
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                account = serializer.save()
                token = Token.objects.get_or_create(user=account)[0].key
                data["message"] = 'User registered successfully'
                data["email"] = account.email
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
