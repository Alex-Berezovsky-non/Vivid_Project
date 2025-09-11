from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _

class DateTypeFilter(SimpleListFilter):
    title = _('Тип даты')
    parameter_name = 'date_type'

    def lookups(self, request, model_admin):
        return [
            ('weekday', _('Будние дни')),
            ('weekend', _('Выходные')),
            ('specific', _('Конкретные даты')),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(date_type=self.value())
        return queryset

    def expected_parameters(self):
        return [self.parameter_name]