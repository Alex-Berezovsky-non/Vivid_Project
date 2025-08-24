from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Album, Photo, Video, ShootingType
from .filters import AlbumFilter

class GalleryView(ListView):
    """Галерея всех альбомов"""
    model = Album
    template_name = 'portfolio/gallery.html'
    context_object_name = 'albums'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Album.objects.filter(is_published=True).prefetch_related('shooting_types')
        self.filter = AlbumFilter(self.request.GET, queryset=queryset)
        return self.filter.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        context['shooting_types'] = ShootingType.objects.filter(is_active=True)
        context['featured_count'] = Album.objects.filter(is_published=True, is_featured=True).count()
        return context

class AlbumDetailView(DetailView):
    """Детальная страница альбома"""
    model = Album
    template_name = 'portfolio/album_detail.html'
    context_object_name = 'album'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Album.objects.filter(is_published=True).prefetch_related('photos', 'shooting_types')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = self.object
        context['photos'] = album.photos.all().order_by('order')
        return context

class VideoListView(ListView):
    """Список всех видео"""
    model = Video
    template_name = 'portfolio/video_list.html'
    context_object_name = 'videos'
    paginate_by = 12
    
    def get_queryset(self):
        return Video.objects.filter(is_published=True).prefetch_related('shooting_types')

class ShootingTypeListView(ListView):
    """Альбомы по типу съемки"""
    template_name = 'portfolio/shooting_type.html'
    context_object_name = 'albums'
    paginate_by = 12
    
    def get_queryset(self):
        self.shooting_type = get_object_or_404(ShootingType, slug=self.kwargs['slug'], is_active=True)
        return Album.objects.filter(
            is_published=True,
            shooting_types=self.shooting_type
        ).prefetch_related('shooting_types')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shooting_type'] = self.shooting_type
        return context

def media_fullscreen(request, photo_id):
    """Полноэкранный просмотр медиа"""
    photo = get_object_or_404(Photo, id=photo_id)
    return render(request, 'portfolio/media_fullscreen.html', {'photo': photo})