from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Assuming 'index' is the view for your homepage
    path('generic/', views.generic, name='generic'),  # URL pattern for the generic.html page
    path('invalid_link/', views.invalid_link, name='invalid_link'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),  # Add this URL pattern for PDF generation
    # Add other URL patterns as needed
]
