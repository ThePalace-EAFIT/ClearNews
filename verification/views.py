from django.shortcuts import render, redirect
from .forms import LinkForm
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('./API.env')

client = OpenAI(api_key = os.environ.get("openai_apikey"))


def verify_link(request):
    form = LinkForm()
    return render(request, 'form.html', {'form': form})


def process_link(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            request.session['url'] = url
            return render(request, 'processing.html', {'url': url})
    return redirect('verify_link')


def show_result(request):
    url = request.session.get('url', None)
    if not url:
        return redirect('verify_link')

    prompt = f"""Analiza la credibilidad de la siguiente noticia basada en su URL: {url}.
    Devuelve un puntaje de credibilidad del 1 al 100 y una breve pero detallada explicación de este puntaje(máx 3 frases)."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un verificador de noticias."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=500,
        )
        result = response.choices[0].message.content.strip()
    except Exception as e:
        result = f"Hubo un error al consultar la API de OpenAI: {str(e)}"

    return render(request, 'ai_result.html', {'url': url, 'result': result})