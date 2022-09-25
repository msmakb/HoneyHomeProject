from django.utils import timezone
import datetime
from .models import Week


def addWeekToRate():
    """
    Add a new week to rate every Sunday
    """
    today = datetime.strftime(timezone.now(), '%Y-%m-%d')
    if str(Week.objects.get(id=Week.getLastWeekID()).week_end_date) != today:
        Week.objects.create(
            week_start_date=today - datetime.timedelta(days=6),
            week_end_date=today
        )
