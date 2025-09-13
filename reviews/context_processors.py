def latest_reviews(request):
    """Добавляет последние отзывы в контекст всех шаблонов"""
    from .models import Review
    
    return {
        'latest_reviews': Review.objects.filter(
            status='approved', 
            is_public=True
        ).order_by('-created_at')[:3]
    }