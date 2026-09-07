from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.marketplace_view, name='marketplace'),
    path('bundle/<slug:slug>/', views.bundle_detail_view, name='bundle_detail'),
    path('bundle/<slug:slug>/checkout/', views.bundle_checkout_view, name='bundle_checkout'),
    path('checkout/<slug:slug>/', views.checkout_view, name='checkout'),
    path('payment/verify/', views.verify_payment, name='verify_payment'),
    path('order-success/<str:order_id>/', views.order_success_view, name='order_success'),
    path('api/check-coupon/', views.check_coupon_api, name='check_coupon'),
    path('user/my-notes/', views.my_notes_view, name='my_notes'),
    path('user/my-orders/', views.my_orders_view, name='my_orders'),
    path('<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('<slug:product_slug>/read/', views.notes_reader_view, name='reader'),
    path('<slug:product_slug>/read/<slug:chapter_slug>/', views.notes_reader_view, name='reader_chapter'),
    path('<slug:product_slug>/chapter/<int:chapter_id>/complete/', views.mark_chapter_complete, name='mark_chapter_complete'),
    path('chapter/<int:chapter_id>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('<slug:slug>/download-pdf/', views.download_notes_pdf, name='download_pdf'),
]
