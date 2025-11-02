"""bhp_personnel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.views.generic.base import RedirectView

from .admin_site import bhp_personnel_admin

app_name = 'bhp_personnel'

urlpatterns = [
    path('administrator/', bhp_personnel_admin.urls),

    path('', RedirectView.as_view(url='administrator/'), name='home_url')

    # Global admin removed - do not mount here
    # path('admin/', admin.site.urls),
]
