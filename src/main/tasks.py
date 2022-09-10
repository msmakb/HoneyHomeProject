from .models import Employee, Task
from datetime import datetime
from django.db.models import Q


class TasksModel:
    def __init__(self, request) -> None:
        self.request = request

    def main(self):
        context = {'Tasks':{}}
        employee = Employee.objects.get(account=self.request.user)
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
                                         'time_left':self.getTimeLeft(task.deadline_date)}
                key+=1
        except: pass 
            #context['Tasks'][1] = {'name':'No Tasks', 'description':'Congratulation you dont have any tasks'}
        return context

    def getTimeLeft(self, deadline):
        date, time = str(deadline.date()).split('-'), str(deadline.time()).split(':')
        date = datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2][:2]), 00000)
        diff = date - datetime.now()
        if str(diff)[0] == '-':
            return 'Deadlined'
        else:
            return str(diff)[:-7]

