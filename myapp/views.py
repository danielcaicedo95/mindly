from django.shortcuts import render, redirect
from .forms import WebsiteForm
from .models import Website
import requests
from bs4 import BeautifulSoup
import openai

# Configura tu clave de API de OpenAI aquí
openai.api_key = "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"

# Vista para la página de inicio
def home(request):
    return render(request, 'home.html')

# Función para obtener el diagnóstico SEO de GPT-3.5 Turbo
def get_seo_diagnosis(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tú eres un asistente de SEO."},
            {"role": "user", "content": text}
        ],
        max_tokens=600
    )
    return response.choices[0].message["content"].strip()

# Función para analizar el HTML de una URL
def analyze_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Realiza el análisis del HTML aquí
        title = soup.find('title')
        meta_description = soup.find('meta', attrs={'name': 'description'})
        # ... Analiza otros elementos del HTML según tus necesidades
        
        # Crea el diagnóstico SEO
        seo_diagnosis = f"Diagnóstico SEO para {url}\n"
        seo_diagnosis += f"Meta Título: {title.text.strip() if title else 'No tiene'}\n"
        seo_diagnosis += f"Meta Descripción: {meta_description['content'] if meta_description else 'No tiene'}\n"
        # ... Agrega más información al diagnóstico según lo analizado
        
        return seo_diagnosis
    except requests.exceptions.RequestException as e:
        return f'Error en la solicitud HTTP: {e}'

# Vista para el diagnóstico SEO
def seo_diagnosis(request):
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            
            # Realiza el análisis del HTML
            seo_diagnosis = analyze_html(url)
            
            # Obtén el diagnóstico SEO de GPT-3.5 Turbo
            seo_diagnosis_with_ai = get_seo_diagnosis(seo_diagnosis)
            
            # Crea un nuevo objeto Website con la URL y el diagnóstico SEO
            website = Website(url=url, seo_diagnosis=seo_diagnosis_with_ai)
            website.save()
            
            return render(request, 'result.html', {'website': website})
    
    else:
        form = WebsiteForm()
    
    return render(request, 'diagnosis.html', {'form': form})
