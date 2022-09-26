from django.db.models import Q
from datetime import datetime
from django.utils import timezone
from human_resources.models import Employee, Task


def getEmployeesTasks(request):
    context = {'Tasks':{}}
    employee = Employee.objects.get(account=request.user)
    Tasks = Task.objects.filter(~Q(status="Late-Submission") & ~Q(status="On-Time"), employee=employee)
    try:
        key = 1
        for task in Tasks:
            context['Tasks'][key] = {'id':task.id, 
                                        'employee':task.employee,
                                        'name':task.name,
                                        'description':task.description,
                                        'status':task.status,
                                        'receiving_date':task.receiving_date,
                                        'deadline_date':task.deadline_date,
                                        'submission_date':task.submission_date,
                                        'time_left':task.getTimeLeft}
            key+=1
    except: pass 
    return context
