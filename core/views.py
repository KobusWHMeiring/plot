from django.shortcuts import render
from django.http import HttpResponse
from core.services import inquiry_service

def home(request):
    return render(request, 'core/home.html')

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
            return HttpResponse('<div class="success-message">Thanks! We will be in touch soon.</div>')
        else:
            return HttpResponse('<div class="error-message">Please provide both name and email.</div>', status=400)
    
    return HttpResponse('Method not allowed', status=405)
