from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from resumes import views as rv

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', rv.home, name='home'),
    path('about/', rv.about, name='about'),
    path('contact/', rv.contact, name='contact'),
    path('templates-page/', rv.templates_page, name='templates_page'),
    path('accounts/', include('accounts.urls')),
    path('resumes/', include('resumes.urls')),
    path('ats/', include('ats_checker.urls')),
    path('dashboard/', include('accounts.dashboard_urls')),
    path('admin-panel/', include('accounts.admin_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
