# users/templatetags/custom_filters.py

from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def days_left(trial_start_date):
    if trial_start_date:
        today = timezone.now()
        trial_end_date = trial_start_date + timezone.timedelta(days=14)
        return (trial_end_date - today).days
    return None
