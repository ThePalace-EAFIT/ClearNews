from django.shortcuts import render

from .models import New


def search_view(request):
    # Obtiene la consulta de búsqueda si existe
    query = request.GET.get('q', '')
    return render(request, 'search.html', {'query': query})


def news_search(request):
    searchTerm = request.GET.get('searchNew')
    if searchTerm:
        news = New.objects.filter(headline__icontains=searchTerm)
        news = New.objects.filter(url__icontains=searchTerm)
    else:
        news = New.objects.all()
    return render(request, 'search_results.html', {'searchTerm': searchTerm, 'name': 'Santiago', 'news': news})


def loading_view(request):
    return render(request, 'loading.html')
