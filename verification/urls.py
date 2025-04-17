from django.urls import path
from . import views

app_name = 'verification'

urlpatterns = [
    path('', views.verify_link, name='verify_link'),
    path('processing/', views.process_link, name='process_link'),
    path('result/', views.show_result, name='show_result'),
]
