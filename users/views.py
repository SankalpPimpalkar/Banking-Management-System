from django.shortcuts import render,redirect
from .models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def register_account(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        existing_user = User.objects.get(email=email)
        
        if existing_user:
            messages.warning(request, 'User already exists with this email')
        else:
            new_user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            new_user.set_password(password)
            new_user.save()        
            return redirect('login_account')
        
    return render(request, 'register.html')

def login_account(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, 'Invalid user credentials')

    return render(request, 'login.html')

@login_required(redirect_field_name='login_account')
def logout_account(request):
    logout(request)
    return redirect('login_account')