import os
import requests
from django.shortcuts import render, redirect
from .forms import LinkForm
from openai import OpenAI
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv('./API.env')

client = OpenAI(api_key = os.environ.get("openai_apikey"))


def verify_link(request):
    form = LinkForm()
    return render(request, 'form.html', {'form': form})


def process_link(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            request.session['url'] = url
            return render(request, 'processing.html', {'url': url})
    return redirect('verification:verify_link')



def show_result(request):
    url = request.session.get('url', None)
    if not url:
        return redirect('verification:verify_link')

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Obtener el texto del artículo
        paragraphs = soup.find_all('p')
        article_text = ' '.join(p.get_text() for p in paragraphs)
        article_text = article_text.strip()
        if len(article_text) > 4000:
            article_text = article_text[:4000]

        # Intentar detectar título
        title = soup.title.string.strip() if soup.title else 'not available'

        # Intentar detectar autor
        author = None
        author_meta = soup.find('meta', attrs={'name': 'author'}) or soup.find('meta', attrs={'property': 'article:author'})
        if author_meta:
            author = author_meta.get('content', None)
        else:
            # Alternativa: buscar un elemento que contenga la palabra "author"
            author_tag = soup.find(attrs={'class': lambda x: x and 'author' in x.lower()})
            if author_tag:
                author = author_tag.get_text().strip()
        if not author:
            author = 'not available'

        # Intentar detectar fecha
        date = None
        date_meta = soup.find('meta', attrs={'property': 'article:published_time'}) or soup.find('meta', attrs={'name': 'date'})
        if date_meta:
            date = date_meta.get('content', None)
        else:
            # Buscar etiquetas <time>
            time_tag = soup.find('time')
            if time_tag and time_tag.get('datetime'):
                date = time_tag['datetime']
            elif time_tag:
                date = time_tag.get_text().strip()
        if not date:
            date = 'not available'

    except Exception as e:
        result = f"Could not get link content: {str(e)}"
        return render(request, 'ai_result.html', {'url': url, 'result': result})

    # Prompt con todos los datos extraídos
    prompt = f"""
News Title: {title}
Author: {author}
Publication Date: {date}

Analyze the following news story and return a credibility score from 1 to 100 based on:
- Source reliability
- Author
- Date of the news story
- Evidence presented in the text

Assign a score from 1 to 25 to each of these, and a short explanation on why this scores.

News Text:
"\"\"
{article_text}
"\"\"

Return the total score (1-100) and a brief explanation (maximum 3 sentences).
"""

    try:
        ai_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in news verification."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=500,
        )
        result = ai_response.choices[0].message.content.strip()
    except Exception as e:
        result = f"There was an error querying the OpenAI API: {str(e)}"

    return render(request, 'ai_result.html', {
        'url': url,
        'result': result,
        'title': title,
        'author': author,
        'date': date,
        'text': article_text
    })
