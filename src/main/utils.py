from django.db.models import Q
from human_resources.models import Employee, Task


def getUserBaseTemplate(request):
    group = request.user.groups.all()[0].name
    base = ""
    for i in str(group).split(' '):
        base += i.lower()
        if str(group).split(' ')[-1] != i:
            base += '_'
    base += '/base.html'
    return base


def getEmployeesTasks(request):
    employee = Employee.objects.get(account=request.user)
    Tasks = Task.objects.filter(~Q(status="Late-Submission") &
                                ~Q(status="On-Time"), employee=employee)

    return Tasks
