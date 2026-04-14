from django.urls import path
from . import views

urlpatterns = [
    path('checker/', views.ats_checker, name='ats_checker'),
    path('history/', views.ats_history, name='ats_history'),
    path('detail/<int:pk>/', views.ats_detail, name='ats_detail'),
]
