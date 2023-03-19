from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request , username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Provide correct username and password')
                return redirect('login')
    return render(request,'login/login.html')


def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST['username']
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            password = request.POST['password']

            if len(password) < 6 :
                messages.error(request, 'Password should be grater than 5 character')
                return redirect('register')

            user = User.objects.create_user(username=username,password=password,email=email)
            user.is_active = True
            user.is_staff = True
            user.first_name = fname
            user.last_name = lname
            user.save()
            if User.objects.filter(username = username).first():
                return redirect('login')
            return redirect('login')

    return render(request,'register/register.html')

def user_logout(request):
    logout(request)
    return redirect('login')

