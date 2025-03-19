from django.shortcuts import render
import requests

from .models import New


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
        api_key = "AIzaSyB1FL2jEMWnoXW7BAsf4VYo3fWdtBsvvgY" 
        api_url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={api_key}"

        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            print(f"Respuesta de la API: {data}")  
        else:
            data = {"error": f"Error {response.status_code}: {response.text}"}
            print(data) 

        return render(request, "results.html", {"query": query, "data": data})

    return render(request, "results.html", {"query": query, "data": None})