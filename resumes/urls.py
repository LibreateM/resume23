from django.urls import path
from . import views

urlpatterns = [
    path('builder/', views.builder, name='builder'),
    path('ai-builder/', views.ai_builder, name='ai_builder'),
    path('<int:pk>/', views.resume_detail, name='resume_detail'),
    path('<int:pk>/edit/', views.resume_edit, name='resume_edit'),
    path('<int:pk>/delete/', views.resume_delete, name='resume_delete'),
    path('<int:pk>/download-pdf/', views.download_pdf, name='download_pdf'),
]
