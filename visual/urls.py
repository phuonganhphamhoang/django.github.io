"""
URL configuration for visual project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from billing import views
from billing.views import json_view, upload_csv, chart_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('json/', json_view, name='json_view'),
    path('visualize/', views.visualize_data, name='visualize_data'),
    path('', upload_csv, name='upload_csv'),
    path('chart/', chart_view, name='chart'),
]

