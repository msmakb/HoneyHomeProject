from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Week, Task, Employee


def addWeekToRate():
    """
    Add a new week to rate every Sunday
    """
    now = timezone.now()
    today = datetime.strftime(timezone.now(), '%Y-%m-%d')
    if str(Week.objects.get(id=Week.getLastWeekID()).week_end_date) != today:
        emp = Employee.objects.get(position='Human Resources')
        Week.objects.create(
            week_start_date= now - timedelta(days=6),
            week_end_date= today
            )
        Task.objects.create(
            employee = emp,
            name = "Evaluate employees",
            description = "Make sure to rate each employee on their weekly evaluations.",
            deadline_date = now + timedelta(days=7)
        )


def checkTaskDateTime():
    """
    Check if the  task is overdue and change it status in database
    """
    Tasks = Task.objects.filter(
        ~Q(status="Late-Submission") & ~Q(status="On-Time"))
    now = datetime.strftime(timezone.now(), '%Y-%m-%d %H:%M:%s')

    for task in Tasks:
        if task.status == "In-Progress":
            if str(task.deadline_date) <= now:
                task.status = "Overdue"
                task.save()
        elif task.status == "Overdue":
            if str(task.deadline_date) >= now:
                task.status = "In-Progress"
                task.save()
