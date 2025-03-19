from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError

def signup_view(request):
    form = UserCreationForm()
    if (request.method == 'GET'):
        return render(request, 'signup.html', {'form': form})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('search')
            except IntegrityError:
                return render(request, 'signup.html', {'form': form, 'error': 'Username is already taken. Choose new username'})
        else:
            return render(request, 'signup.html', {'form': form, 'error': 'Passwords did not match'})
        
def logout_view(request):
    logout(request)
    return redirect('search')

def login_view(request):
    form = AuthenticationForm()
    if request.method == 'GET':
        return render(request, 'login.html', {'form': form})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {'form': form, 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('search')
