from django.shortcuts import render

def search_view(request):
    query = request.GET.get('q', '')  # Obtiene la consulta de búsqueda si existe
    return render(request, 'search.html', {'query': query})
