from django.db.models import Q
from human_resources.models import Employee, Task


def getEmployeesTasks(request):
    employee = Employee.objects.get(account=request.user)
    Tasks = Task.objects.filter(~Q(status="Late-Submission") &
                                ~Q(status="On-Time"), employee=employee)

    return Tasks
