from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='home'),
    path('login/', views.Login,name='Login'),
    path('signup/', views.signup,name='signUp'),
    path('logout/', views.Logout,name='logout'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('api/receiveLogs/', views.receiveLogs),
]
