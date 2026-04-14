from django.urls import path
from . import admin_views

urlpatterns = [
    path('', admin_views.admin_dashboard, name='admin_dashboard'),
    path('users/', admin_views.admin_users, name='admin_users'),
    path('users/<int:user_id>/toggle/', admin_views.toggle_user, name='toggle_user'),
    path('resumes/', admin_views.admin_resumes, name='admin_resumes'),
    path('resumes/<int:resume_id>/delete/', admin_views.delete_resume_admin, name='delete_resume_admin'),
    path('ats/', admin_views.admin_ats, name='admin_ats'),
]
