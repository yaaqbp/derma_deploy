from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'image_classification'

urlpatterns = [
    path('', views.index, name='index'),
    path('diseases/', views.diseases, name='diseases'),
    path('about/', views.about, name='about'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
