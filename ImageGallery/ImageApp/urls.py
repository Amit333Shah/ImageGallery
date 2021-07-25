from django.conf.urls.static import static
from django.conf import settings
from django import urls
from django.urls import path
from.import views

urlpatterns = [
    path('', views.imageView, name="home"),
    path('post/<slug:slug>/', views.detail_view, name="detail"),
    path('tag/<slug:slug>/', views.tagged, name="tagged"),
    path('listpage', views.listPage, name="listpage"),
    path('rotateleft/', views.rotateLeft, name="rotateleft"),
    path('rotateright/', views.rotateRight, name="rotateright")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
