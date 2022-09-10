from django.shortcuts import redirect, render
from .forms import AddPersonForm, GetEmployeePosition, AddTaskForm
from .Evaluation import Evaluation
from django.apps import apps
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from main.models import Person, Employee, Distributor, Task, TaskRate, Week, WeeklyRate, Stock
from main.decorators import allowed_users
from main.tasks import TasksModel
from main.utils import getUserBaseTemplate as base


# ------------------------------Dashboard------------------------------
@allowed_users(['Human Resources'])
def humanResourcesDashboard(request):
    context = {'TasksModel':TasksModel(request)}
    return render(request, 'human_resources/dashboard.html', context)

# ------------------------------Employees------------------------------
def EmployeesPage(request):
    Employees = Employee.objects.all()
    
    context = {'Employees': Employees, 'base': base(request), 'TasksModel':TasksModel(request)}
    return render(request, 'human_resources/employees.html', context)

def AddEmployeePage(request):
    person_form = AddPersonForm()
    position_form = GetEmployeePosition()
    if request.method == 'POST':
        person_form = AddPersonForm(request.POST)
        position_form = GetEmployeePosition(request.POST)
        if person_form.is_valid() and position_form.is_valid():
            person_form.save()
            person = Person.objects.all().order_by('-id')[0]
            User.objects.create_user(username=str(person.name).split(' ')[0],
                                    email=person.contacting_email,
                                    password=str(person.name).split(' ')[0],
                                    first_name=str(person.name).split(' ')[0],
                                    last_name=str(person.name).split(' ')[-1],
                                    ).save()
            account = User.objects.all().order_by('-id')[0]
            position = position_form['position'].value()
            Group.objects.get(name=position).user_set.add(account)
            Employee.objects.create(person=person, account=account, position=position)
            return redirect('EmployeesPage')

    context = {'PersonForm':person_form, 'position_form':position_form, 'base':base(request), 'TasksModel':TasksModel(request)}
    return render(request, 'human_resources/add_employee.html', context) 

def EmployeePage(request, pk):
    from django import template

    employee = Employee.objects.get(id=pk)
    evaluation = Evaluation(Employee, Task, TaskRate, Week, WeeklyRate).evaluation(emp_id=pk)
    context = {'Employee': employee, 'Evaluation':evaluation, 'base':base(request), 'TasksModel':TasksModel(request)}
    return render(request, 'human_resources/employee.html', context) 

def UpdateEmployeePage(request, pk):
    employee = Employee.objects.get(id=pk)
    position_form = GetEmployeePosition(instance=employee)
    person = Person.objects.get(id=employee.person.id)
    person_form = AddPersonForm(instance=person)
    if request.method == 'POST':
        person_form = AddPersonForm(request.POST, instance=person)
        position_form = GetEmployeePosition(request.POST, instance=employee)
        if person_form.is_valid() and position_form.is_valid():
            person_form.save()
            position_form.save()
            position = position_form['position'].value()
            employee.account.groups.clear()
            Group.objects.get(name=position).user_set.add(employee.account)
            return redirect('EmployeePage', pk)
    
    context = {'PersonForm':person_form, 'position_form':position_form, 'Employee':employee, 'base':base(request), 'TasksModel':TasksModel(request)}
    return render(request, 'human_resources/update_employee.html', context) 

def DeleteEmployeePage(request, pk):
    employee = Employee.objects.get(id=pk)
    if request.method == "POST":
        employee.account.delete()
        employee.delete()
        return redirect('EmployeesPage')
    context= {'Employee':employee, 'base':base(request), 'TasksModel':TasksModel(request)}
    return render(request, 'human_resources/delete_employee.html', context)

# ------------------------------Distributors------------------------------
def DistributorsPage(request):
    Distributors = Distributor.objects.all()
    context = {'Distributors': Distributors, 'base':base(request), 'TasksModel':TasksModel(request)}
    return render(request, 'human_resources/distributors.html', context)

def AddDistributorPage(request):
    person_form = AddPersonForm()
    if request.method == 'POST':
        person_form = AddPersonForm(request.POST)
        if person_form.is_valid():
            person_form.save()
            person = Person.objects.all().order_by('-id')[0]
            User.objects.create_user(username=str(person.name).split(' ')[0],
                                    email=person.contacting_email,
                                    password=str(person.name).split(' ')[0],
                                    first_name=str(person.name).split(' ')[0],
                                    last_name=str(person.name).split(' ')[-1],
                                    ).save()
            account = User.objects.all().order_by('-id')[0]
            Group.objects.get(name="Distributor").user_set.add(account)
            Stock.objects.create()
            stock = Stock.objects.all().order_by('-id')[0]
            Distributor.objects.create(person=person, account=account, stock=stock)
            return redirect('DistributorsPage')

    context = {'PersonForm':person_form, 'base':base(request), 'TasksModel':TasksModel(request)}
    return render(request, 'human_resources/add_distributor.html', context) 

def DistributorPage(request, pk):
    distributor = Distributor.objects.get(id=pk)
    context = {'Distributor': distributor, 'base':base(request), 'TasksModel':TasksModel(request)}
    return render(request, 'human_resources/distributor.html', context) 

def UpdateDistributorPage(request, pk):
    distributor = Distributor.objects.get(id=pk)
    person = Person.objects.get(id=distributor.person.id)
    person_form = AddPersonForm(instance=person)
    if request.method == 'POST':
        person_form = AddPersonForm(request.POST, instance=person)
        if person_form.is_valid():
            person_form.save()
            return redirect('DistributorPage', pk)
    
    context = {'PersonForm':person_form, 'Distributor':distributor, 'base':base(request), 'TasksModel':TasksModel(request)}
    return render(request, 'human_resources/update_distributor.html', context) 

def DeleteDistributorPage(request, pk):
    distributor = Distributor.objects.get(id=pk)
    if request.method == "POST":
        distributor.account.delete()
        distributor.delete()
        return redirect('DistributorsPage')
    context = {'Distributor':distributor, 'base':base(request), 'TasksModel':TasksModel(request)}
    return render(request, 'human_resources/delete_distributor.html', context)

# ------------------------------Tasks------------------------------
def TasksPage(request):
    Tasks = Task.objects.all()
    context = {'Tasks':Tasks, 'base':base(request), 'TasksModel':TasksModel(request)}
    return render(request, 'human_resources/tasks.html', context)

def AddTaskPage(request):
    form = AddTaskForm()
    if request.method == "POST":
        form = AddTaskForm(request.POST)
        if form.is_valid():
            form.save()
            q = Task.objects.all().order_by('-id')[0]
            q.status = 'In-Progress'
            q.save()
            return redirect('TasksPage')

    context = {'form':form, 'base':base(request), 'TasksModel':TasksModel(request)}
    return render(request, 'human_resources/add_task.html', context)

def TaskPage(request, pk):
    task = Task.objects.get(id=pk)
    try:
        task_rate = TaskRate.objects.get(task=task)
    except TaskRate.DoesNotExist:
        task_rate = None
    context = {'Task':task, 'TaskRate':task_rate, 'base':base(request), 'TasksModel':TasksModel(request)}
    return render(request, 'human_resources/task.html', context) 

def UpdateTaskPage(request, pk):
    task = Task.objects.get(id=pk)
    form = AddTaskForm(instance=task)
    if request.method == 'POST':
        form = AddTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('TaskPage', pk)
    context = {'form':form, 'TaskID':task.id, 'base':base(request),'TasksModel':TasksModel(request)}
    return render(request, 'human_resources/update_task.html', context) 

def DeleteTaskPage(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == "POST":
        task.delete()
        return redirect('TasksPage')
    context = {'Task':task, 'base':base(request), 'TasksModel':TasksModel(request)}
    return render(request, 'human_resources/delete_Task.html', context)

# ------------------------------Evaluation------------------------------
def EvaluationPage(request):
    evaluation = Evaluation(Employee, Task, TaskRate, Week, WeeklyRate).evaluation()
    context = {'Evaluation':evaluation, 'base':base(request), 'TasksModel':TasksModel(request)}
    return render(request, 'human_resources/evaluation.html', context)

def WeeklyEvaluationPage(request):
    weeks = Week.objects.filter(is_rated=False)
    Employees = Employee.objects.filter(~Q(position="CEO") & ~Q(position="Human Resources"))
    context = {'base':base(request), 'TasksModel':TasksModel(request)}
    if not weeks.exists():
        messages.info(request, "Weekly evaluation has been don")
    else:
        context['Employees'] = Employees
    if request.method == "POST":
        for emp in Employees:
            val = request.POST.get(f'val{str(emp.id)}', False)
            WeeklyRate.objects.create(
                                      week=weeks[0],
                                      employee=emp,
                                      rate=int(val))
        q = weeks[0]
        q.is_rated = True
        q.save()
        task = Task.objects.get(id=8)
        task.is_rated = True
        task.status = "On-Time"
        task.save()

        return redirect('EvaluationPage')

    return render(request, 'human_resources/weekly_rate.html', context)

def TaskEvaluationPage(request):
    Tasks = Task.objects.filter(~Q(status="In-Progress") & ~Q(status="Deadlined"), is_rated=False)
    if request.method == "POST":
        id = request.POST.get('id', False)
        val = request.POST.get(f'val{str(id)}', False)
        on_time = 5
        task = Task.objects.get(id=int(id))
        if task.status != "On-Time": 
            on_time = 2.5
        TaskRate.objects.create(task=task, on_time_rate=on_time, rate=int(val))
        task.is_rated = True
        task.save()

        messages.success(request, f"Task has been rated successfuly")
    if not Tasks.exists():
        messages.info(request, "There is no more tasks to rate") 

    #print(Tasks[0].name)
    context = {'Tasks':Tasks,  'base':base(request), 'TasksModel':TasksModel(request)}
    return render(request, 'human_resources/task_evaluation.html', context)
