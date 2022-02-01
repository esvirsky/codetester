"""codetester URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from fluent_blogs.sitemaps import EntrySitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'blog_entries': EntrySitemap,
}

urlpatterns = [
    path('', include(('general.urls', 'general'), namespace='general')),
    path('assessment/', include(('assessment.urls', 'assessment'), namespace='assessment')),
    path('runner/', include(('runner.urls', 'runner'), namespace='runner')),
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^blog/', include('fluent_blogs.urls')),
    url(r'^sitemap.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
