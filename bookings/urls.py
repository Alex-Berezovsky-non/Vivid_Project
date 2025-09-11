from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.TimeSlotSelectionView.as_view(), name='calendar'),
    path('slot/<int:slot_id>/', views.BookingCreateView.as_view(), name='booking_create'),
    path('done/<str:code>/', views.BookingDoneView.as_view(), name='booking_done'),
    path('booking/<str:code>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('status/', views.BookingStatusView.as_view(), name='booking_status'),
]