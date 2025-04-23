from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.db.models import Avg
from verification.models import AnalyzedNews

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
        
@login_required
def dashboard(request):
    user_news = AnalyzedNews.objects.filter(user=request.user).order_by('-created_at')

    total_news = user_news.count()
    average_score = user_news.aggregate(avg_score=Avg('score'))['avg_score'] or 0
    average_score = round(average_score)

    context = {
        'news_list': user_news,
        'total_news': total_news,
        'average_score': average_score,
    }
    return render(request, 'dashboard.html', context)
