import os, re
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import VerificationForm
from openai import OpenAI
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from .models import AnalyzedNews
from datetime import datetime

load_dotenv('./API.env')

client = OpenAI(api_key = os.environ.get("openai_apikey"))


def verify_link(request):
    form = VerificationForm()
    return render(request, 'form.html', {'form': form})

def process_link(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data.get('url', '').strip()
            text = form.cleaned_data.get('text', '').strip()
            request.session['url'] = url or ''
            request.session['text'] = text or ''
            return render(request, 'processing.html', {'url': url if url else None})
        else:
            # Form no válido
            return render(request, 'form.html', {'form': form})
    return redirect('verification:verify_link')


@login_required
def show_result(request):
    url = request.session.get('url', '')
    text = request.session.get('text', '')

    if url:  # Si viene de un enlace
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Obtener el texto del artículo
            paragraphs = soup.find_all('p')
            article_text = ' '.join(p.get_text() for p in paragraphs).strip()
            if len(article_text) > 4000:
                article_text = article_text[:4000]

            title = soup.title.string.strip() if soup.title else 'not available'

            # Detectar autor
            author = None
            author_meta = soup.find('meta', attrs={'name': 'author'}) or soup.find('meta', attrs={'property': 'article:author'})
            if author_meta:
                author = author_meta.get('content', None)
            else:
                author_tag = soup.find(attrs={'class': lambda x: x and 'author' in x.lower()})
                author = author_tag.get_text().strip() if author_tag else 'not available'

            # Detectar fecha
            date = None
            date_meta = soup.find('meta', attrs={'property': 'article:published_time'}) or soup.find('meta', attrs={'name': 'date'})
            if date_meta:
                date = date_meta.get('content', None)
            else:
                time_tag = soup.find('time')
                if time_tag and time_tag.get('datetime'):
                    date = time_tag['datetime']
                elif time_tag:
                    date = time_tag.get_text().strip()
            if not date:
                date = 'not available'
            else:
                try:
                    parsed_date = datetime.fromisoformat(date.replace('Z', '+00:00')) 
                    date = parsed_date.strftime('%d %B %Y, %H:%M') 
                except ValueError:
                    pass

        except Exception as e:
            result = f"Could not get link content: {str(e)}"
            return render(request, 'ai_result.html', {'url': url, 'result': result})

    elif text:  # Si viene de texto plano
        article_text = text.strip()
        if len(article_text) > 4000:
            article_text = article_text[:4000]
        title = 'Provided directly'
        author = 'not available'
        date = 'not available'

    else:
        return redirect('verification:verify_link')

    # Prompt para OpenAI

    # Idioma del usuario
    idioma = request.LANGUAGE_CODE

    if idioma == 'es':
        lang_instruction = "Responde en español."
    elif idioma == 'pt':
        lang_instruction = "Responda em português."
    else:
        lang_instruction = "Respond in English."



    prompt = f"""{lang_instruction}
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
        \"\"\"
        {article_text}
        \"\"\"

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

    score_match = re.search(r"(?:Total Score|Score total)[:\s]*([0-9]{1,3})", result, re.IGNORECASE)
    score = int(score_match.group(1)) if score_match else 0

    AnalyzedNews.objects.create(
        user=request.user,
        title=title,
        author=author,
        date=date,
        url=url or None,
        text=article_text,
        score=score,
        explanation=result
    )


    return render(request, 'ai_result.html', {
        'url': url,
        'result': result,
        'title': title,
        'author': author,
        'date': date,
        'text': article_text,
    })

