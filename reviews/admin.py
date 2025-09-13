from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from .models import Review, SocialReview

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author', 'rating_stars', 'status_badge', 'status', 'created_at', 'is_public']
    list_editable = ['status', 'is_public']
    list_filter = ['status', 'rating', 'created_at', 'is_public']
    search_fields = ['author', 'email', 'text']
    readonly_fields = ['created_at']
    actions = ['approve_selected', 'reject_selected', 'make_public', 'make_private']
    
    fieldsets = (
        (_('Информация об авторе'), {
            'fields': ('author', 'email')
        }),
        (_('Содержание отзыва'), {
            'fields': ('rating', 'text', 'photo')
        }),
        (_('Статус и видимость'), {
            'fields': ('status', 'is_public', 'created_at')
        }),
    )
    
    def rating_stars(self, obj):
        return '★' * obj.rating + '☆' * (5 - obj.rating)
    rating_stars.short_description = _('Оценка')
    
    def status_badge(self, obj):
        colors = {'pending': 'orange', 'approved': 'green', 'rejected': 'red'}
        return mark_safe(f'<span style="color: {colors[obj.status]};">{obj.get_status_display()}</span>')
    status_badge.short_description = _('Статус')
    status_badge.allow_tags = True
    
    def approve_selected(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f"{updated} отзывов одобрено")
    approve_selected.short_description = _('Одобрить выбранные')
    
    def reject_selected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f"{updated} отзывов отклонено")
    reject_selected.short_description = _('Отклонить выбранные')
    
    def make_public(self, request, queryset):
        updated = queryset.update(is_public=True)
        self.message_user(request, f"{updated} отзывов сделано публичными")
    make_public.short_description = _('Сделать публичными')
    
    def make_private(self, request, queryset):
        updated = queryset.update(is_public=False)
        self.message_user(request, f"{updated} отзывов сделано приватными")
    make_private.short_description = _('Сделать приватными')

@admin.register(SocialReview)
class SocialReviewAdmin(admin.ModelAdmin):
    list_display = ['author', 'source', 'rating_stars', 'created_at', 'imported_at']
    list_filter = ['source', 'rating', 'created_at']
    search_fields = ['author', 'text', 'external_id']
    readonly_fields = ['imported_at', 'external_id', 'post_url', 'photo_url']
    
    fieldsets = (
        (_('Источник'), {
            'fields': ('source', 'external_id')
        }),
        (_('Содержание'), {
            'fields': ('author', 'text', 'rating')
        }),
        (_('Ссылки и медиа'), {
            'fields': ('photo_url', 'post_url')
        }),
        (_('Даты'), {
            'fields': ('created_at', 'imported_at')
        }),
    )
    
    def rating_stars(self, obj):
        return '★' * obj.rating + '☆' * (5 - obj.rating)
    rating_stars.short_description = _('Оценка')
    
    def has_add_permission(self, request):
        return False  # Запрещаем ручное добавление социальных отзывов