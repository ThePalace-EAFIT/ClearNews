from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),  
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]