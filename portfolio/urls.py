from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.GalleryView.as_view(), name='gallery'),
    path('album/<slug:slug>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('videos/', views.VideoListView.as_view(), name='video_list'),
    path('type/<slug:slug>/', views.ShootingTypeListView.as_view(), name='shooting_type'),
    path('media/<int:photo_id>/fullscreen/', views.media_fullscreen, name='media_fullscreen'),
]