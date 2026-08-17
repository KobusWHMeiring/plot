from django.http import Http404, HttpResponse
from django.shortcuts import render

from core.services import inquiry_service


PROJECTS = [
    {'slug': 'harvester', 'name': 'Harvester', 'tagline': 'Urban garden & landscaping operations'},
    {'slug': 'river', 'name': 'River', 'tagline': 'Field-operations system for river rehabilitation'},
    {'slug': 'farm', 'name': 'Farm', 'tagline': 'Farm management for a regenerative farm'},
]

CASE_STUDY_TEMPLATES = {
    'harvester': 'core/work/harvester.html',
    'river': 'core/work/river.html',
    'farm': 'core/work/farm.html',
}


def home(request):
    return render(request, 'core/home.html')


def work_detail(request, slug):
    template = CASE_STUDY_TEMPLATES.get(slug)
    if template is None:
        raise Http404
    return render(request, template, {
        'slug': slug,
        'projects': [p for p in PROJECTS if p['slug'] != slug],
    })

def submit_inquiry(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        company_name = request.POST.get('company_name')
        message = request.POST.get('message')
        
        if name and email:
            inquiry_service.create_pilot_inquiry(
                name=name,
                email=email,
                company_name=company_name,
                message=message
            )
            return HttpResponse('<div class="success-message">Thanks! I\'ll be in touch soon.</div>')
        else:
            return HttpResponse('<div class="error-message">Please provide both name and email.</div>', status=400)
    
    return HttpResponse('Method not allowed', status=405)
