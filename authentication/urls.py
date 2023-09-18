from django.urls import path
from . import views
from .views import AllUsers
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'authentication'

urlpatterns = [
    path('create/', views.create_user, name='register_user'),
    #   path('login/', ObtainAuthTokenView.as_view(), name='token_view'),
    path('users/', AllUsers.as_view(), name='users'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
