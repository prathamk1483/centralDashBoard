from django.urls import path
from .views import receiveLogs

urlpatterns = [
    path('api/receiveLogs/', receiveLogs),
]
