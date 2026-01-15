from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit-inquiry/', views.submit_inquiry, name='submit_inquiry'),
]