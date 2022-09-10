from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .decorators import unauthenticaredUser
from .models import Employee, Task
from .tasks import TasksModel
from .utils import getUserBaseTemplate

# Create your views here.
@unauthenticaredUser
def index(request):
    if request.method == "POST":
        UserName = request.POST.get('user_name')
        Password = request.POST.get('password')
        User = authenticate(request, username=UserName, password=Password)

        if User is not None:
            login(request, User)
            return redirect('index')
        else:
            messages.info(request, "Username or Password is incoorect")

    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def unauthorized(request):
    return render(request, 'unauthorized.html')

@login_required(login_url='index')
def Dashboard(request):
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    return render(request, 'Dashboard.html', {'group': group})

def logoutUser(request):
    logout(request)
    return redirect(index)

def Tasks(request):
    Tasks = Task.objects.filter(~Q(status="Late-Submission") & ~Q(status="On-Time"), employee=Employee.objects.get(account=request.user))
    base = getUserBaseTemplate(request)

    if request.method == "POST":
        print('gg')
        id = request.POST.get('task_id', False)
        onTime= request.POST.get(f'onTime{id}', False)
        print(id, onTime)
        if onTime == "True":
            onTime = "On-Time"
        else:
            onTime = "Late-Submission"
        task = Task.objects.get(id=int(id))
        task.status = onTime
        task.save()

    context = {'Tasks':Tasks, 'base':base, 'TasksModel':TasksModel(request)}
    return render(request, 'tasks.html', context)
