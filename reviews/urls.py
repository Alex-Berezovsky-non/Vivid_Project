from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.ReviewListView.as_view(), name='list'),
    path('create/', views.ReviewCreateView.as_view(), name='create'),
    path('moderate/', views.ReviewModerateView.as_view(), name='moderate'),
    path('thanks/', views.ReviewThanksView.as_view(), name='thanks'),
]