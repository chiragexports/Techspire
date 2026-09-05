from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('faqs/', views.faq_view, name='faq'),
    path('faq/', views.faq_view, name='faqs'),
    path('privacy-policy/', views.privacy_view, name='privacy'),
    path('terms-and-conditions/', views.terms_view, name='terms'),
    path('newsletter-subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]
