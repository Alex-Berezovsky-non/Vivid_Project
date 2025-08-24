import django_filters
from .models import Album, ShootingType

class AlbumFilter(django_filters.FilterSet):
    shooting_type = django_filters.ModelChoiceFilter(
        field_name='shooting_types',
        queryset=ShootingType.objects.filter(is_active=True),
        label="Тип съемки",
        empty_label="Все типы"
    )
    
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Название"
    )
    
    is_featured = django_filters.BooleanFilter(
        label="Только рекомендуемые"
    )

    class Meta:
        model = Album
        fields = ['shooting_type', 'title', 'is_featured']