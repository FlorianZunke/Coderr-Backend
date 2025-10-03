from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import RegistrationSerializer, CustomLoginSerializer


class RegistrationView(APIView):
        """
        View for user registration.
        """
        permission_classes = [AllowAny]
        
        def post(self, request, *args, **kwargs):
                """
                Handle user registration.
                """
                serializer = RegistrationSerializer(data=request.data)

                if serializer.is_valid():
                        saved_account = serializer.save()
                        token, created = Token.objects.get_or_create(user=saved_account)
                        data = {
                                'token': token.key,
                                'username': saved_account.username,
                                'email': saved_account.email,
                                'user_id': saved_account.id
                                }
                        return Response(data, status=status.HTTP_201_CREATED)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(ObtainAuthToken):
    """
    View for user login.
    """
    permission_classes = [AllowAny]
    serializer_class = CustomLoginSerializer

    def post(self, request):
        """
        Handle user login.
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id,
            }
            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)