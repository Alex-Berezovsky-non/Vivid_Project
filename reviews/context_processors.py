from .models import Review

def latest_reviews(request):
    """Добавляет последние отзывы в контекст всех шаблонов"""
    return {
        'latest_reviews': Review.objects.filter(
            status='approved', 
            is_public=True
        ).order_by('-created_at')[:5]  # Берем 5 последних отзывов
    }