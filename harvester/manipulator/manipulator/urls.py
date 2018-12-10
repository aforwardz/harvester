"""manipulator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
admin.site.site_header = '「Harvester」'

api_patterns = [
    path('api/account/', include('account.api.urls')),
]

urlpatterns = [
    path(r'jet/', include(('jet.urls', 'jet'), 'jet')),
    path('admin/', admin.site.urls),
    path('nlp/', include('nlp.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.WEB_URL, document_root=settings.WEB_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + api_patterns
