"""
URL configuration for djangoAdminNetwork project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from networkProvisioning.views import actions, getConfig, upload_router_data
from ztp.views import monitor_docker_containers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('actions/', actions),
    path('getConfig', getConfig, name='getConfig'),
    path('ztp/', monitor_docker_containers, name='monitor_docker_containers'),
    path('upload/', upload_router_data, name='upload_router_data'  )
]



if settings.DEBUG:
    #AL: Allow file download of template files directly from admin interface in debug mode. Probably bypassing logon
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #AL Temp PoC path to generate config until UUID endpoint is implemented. Not working for some reason
    #urlpatterns.append(path('getConfig/', getConfig, name='getConfig'))
