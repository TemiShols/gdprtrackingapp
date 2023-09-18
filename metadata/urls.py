from django.urls import path
from .views import analyze_chrome, GetChromeView
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'metadata'

urlpatterns = [
    path('analyze/', analyze_chrome, name='analyze'),
    path('chrome/<int:pk>/', GetChromeView.as_view(), name='chrome_view'),
]

urlpatterns = format_suffix_patterns(urlpatterns)