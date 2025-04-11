from rest_framework.decorators import api_view
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def Login(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            print("user is authenticated")
            return redirect('dashboard')  

        if request.method == 'POST':
            email = request.POST.get('userEmail')
            password = request.POST.get('userPassword')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                print("User is authenticated")
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
                return redirect('Login')

    return render(request, 'login.html')

@csrf_exempt
def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('createUserEmail')
        password = request.POST.get('createUserPassword')
        confirm_password = request.POST.get('confirmCreateUserPassword')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signUp')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('signUp')

        user = User.objects.create_user(username=email, email=email, password=password)
        login(user)
        return redirect('dashboard')

    return render(request, 'signup.html')



def Logout(request):
    logout(request)
    return redirect('Login')


def index(request):
    return redirect('Login')

@login_required
def dashboard(request):
    return render(request,"home.html")

@login_required
@api_view(["POST"])
def receiveLogs(request):
    data = request.data
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "log_group",
        {
            "type": "send_log",
            "data": data
        }
    )
    return Response({"message": "Data sent via WebSocket"})
