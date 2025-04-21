from django.shortcuts import render
import requests
import os
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required   

from .models import New

load_dotenv('./API.env')

def search_view(request):
    query = request.GET.get('q', '')
    return render(request, 'search.html', {'query': query})

def search(request):
    return render(request, 'about.html')

def news_search(request):
    searchTerm = request.GET.get('searchNew')
    if searchTerm:
        news = New.objects.filter(headline__icontains=searchTerm)
        news = New.objects.filter(url__icontains=searchTerm)
    else:
        news = New.objects.all()
    return render(request, 'search_results.html', {'searchTerm': searchTerm, 'name': 'Santiago', 'news': news})

def loading_view(request):
    query = request.GET.get("verifyNew", "").strip()

    if query:
        api_key = os.environ.get("google_apikey")
        api_url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={api_key}&languageCode=es&languageCode=en&languageCode=pt"

        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            print(f"Respuesta de la API: {data}")

        else:
            data = {"error": f"Error calling the API: {response.status_code} - {response.text}"}
            print(data) 

        return render(request, "results.html", {"query": query, "results": data.get("claims", [])})

    return render(request, "results.html", {"query": query, "results": None})

def home_view(request):
    api_key = os.environ.get("google_apikey")
    latest_news = []

    if api_key:
        api_url = (
            "https://factchecktools.googleapis.com/v1alpha1/claims:search"
            f"?key={api_key}&query=news&languageCode=es&languageCode=en&languageCode=pt&pageSize=5"
        )

        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            print(f"🔍 Respuesta de la API en home_view: {data}")
            latest_news = data.get("claims", [])
        else:
            print(f"❌ Error al llamar a la API: {response.status_code} - {response.text}")
            latest_news = []
    else:
        print("⚠️ Clave API de Google no encontrada en el entorno")

    return render(request, 'home.html', {
        'authenticated': request.user.is_authenticated,
        'user': request.user,
        'latest_news': latest_news
    })