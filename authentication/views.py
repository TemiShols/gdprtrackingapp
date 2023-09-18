from rest_framework import status
from rest_framework.response import Response
from .models import CustomUser
from .serializer import UserSerializer
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth import authenticate
from rest_framework_api_key.models import APIKey
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@api_view(['POST', ])
def create_user(request):
    if request.method == 'POST':
        data = {}
        email = request.data.get('email', '0').lower()
        if validate_email(email) is not None:
            data['error_message'] = 'That email is already in use.'
            data['response'] = 'Error'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            data['response'] = 'successfully registered new user.'
            data['email'] = serializer.data['email']
            data['first_name'] = serializer.data['first_name']
            data['last_name'] = serializer.data['last_name']
            serializer.save()
            #   user = CustomUser.objects.get(email=email)
            api_key, key = APIKey.objects.create_key(name="my-remote-service")
            data['API KEY'] = key
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


def validate_email(email):
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return None
    if user is not None:
        return email


#   class ObtainAuthTokenView(APIView):
#       authentication_classes = []
#       permission_classes = []

#       def post(self, request):
#           data = {}
#           email = request.POST.get('email')
#           password = request.POST.get('password')
#           account = authenticate(email=email, password=password)
#           if account:
#               try:
#                   token = Token.objects.get(user=account)
#               except Token.DoesNotExist:
#                   token = Token.objects.create(user=account)
#               data['response'] = 'Successfully authenticated.'
#               data['pk'] = account.pk
#               data['email'] = email.lower()
#               data['token'] = token.key
#               return Response(data, status=status.HTTP_200_OK)
#           else:
#               data['response'] = 'Error'
#               data['error_message'] = 'Invalid credentials'
#            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class AllUsers(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [HasAPIKey]
    authentication_classes = []
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('first_name',)
    pagination_class = PageNumberPagination
