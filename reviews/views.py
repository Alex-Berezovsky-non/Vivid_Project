from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .models import Review, SocialReview
from .forms import ReviewForm

class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/list.html'
    context_object_name = 'reviews'
    paginate_by = 10
    
    def get_queryset(self):
        return Review.objects.filter(status='approved', is_public=True).select_related()

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/create.html'
    success_url = reverse_lazy('reviews:list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 
            _("Спасибо за ваш отзыв! Он будет опубликован после модерации.")
        )
        return response

class ReviewModerateView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'reviews/moderate.html'
    context_object_name = 'reviews'
    
    def get_queryset(self):
        return Review.objects.filter(status='pending')
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        review_id = request.POST.get('review_id')
        
        if action and review_id:
            review = get_object_or_404(Review, id=review_id)
            if action == 'approve':
                review.status = 'approved'
                messages.success(request, f"Отзыв от {review.author} одобрен")
            elif action == 'reject':
                review.status = 'rejected'
                messages.warning(request, f"Отзыв от {review.author} отклонен")
            review.save()
        
        return redirect('reviews:moderate')

class ReviewThanksView(TemplateView):
    template_name = 'reviews/thanks.html'