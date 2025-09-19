from django.views.generic import TemplateView, ListView, FormView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .models import SiteSettings, Service
from .forms import ContactForm
from portfolio.models import Photo  # Импортируем модель фото

class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.load()
        context['services'] = Service.objects.filter(is_active=True)[:3]  # 3 последние услуги
        
        # ДОБАВЛЯЕМ СЛУЧАЙНЫЕ ФОТО ДЛЯ ГАЛЕРЕИ (8 штук)
        context['gallery_photos'] = Photo.objects.filter(
            album__is_published=True
        ).order_by('?')[:8]  # order_by('?') - случайный порядок
        
        return context

class AboutView(TemplateView):
    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.load()
        return context

class ServicesView(ListView):
    model = Service
    template_name = "core/services.html"
    context_object_name = "services"

    def get_queryset(self):
        return Service.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.load()
        return context

class ContactView(SuccessMessageMixin, FormView):
    template_name = "core/contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy('core:contacts')
    success_message = "Сообщение отправлено! Я свяжусь с вами в ближайшее время."

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.load()
        return context