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
    path('refund-and-cancellation-policy/', views.refund_policy_view, name='refund_policy'),
    path('refund-policy/', views.refund_policy_view, name='refunds'),
    path('newsletter-subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),

]
