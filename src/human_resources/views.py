from re import T
from django.contrib import messages
from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import redirect, render

from distributor.models import Distributor
from main.decorators import allowed_users
from main.models import Person
from main.tasks import getEmployeesTasks
from main.utils import getUserBaseTemplate as base

from .evaluation import getEvaluation
from .forms import AddPersonForm, EmployeePositionForm, AddTaskForm
from .models import Employee, Task, TaskRate, Week, WeeklyRate


# ------------------------------Dashboard------------------------------ #
@allowed_users(['Human Resources'])
def humanResourcesDashboard(request):

    context = {'getEmployeesTasks': getEmployeesTasks(request)}
    template = 'human_resources/dashboard.html'
    return render(request, template, context)


# ------------------------------Employees------------------------------ #
def EmployeesPage(request):
    # Fetch all employees' data from database
    Employees = Employee.objects.all()

    context = {'Employees': Employees, 'base': base(request),
               'getEmployeesTasks': getEmployeesTasks(request)}
    template = 'human_resources/employees.html'
    return render(request, template, context)


def AddEmployeePage(request):
    # Setting up the forms
    person_form = AddPersonForm()
    position_form = EmployeePositionForm()
    # Check if it is a post method
    if request.method == 'POST':
        person_form = AddPersonForm(request.POST)
        position_form = EmployeePositionForm(request.POST)
        # If the forms are valid
        if person_form.is_valid() and position_form.is_valid():
            # Create person
            person_form.save()
            # Add new employee
            position = position_form['position'].value()
            # Create new employee and a signal will be sent to run onAddingNewEmployee function in signals.py file
            Employee.objects.create(position=position)

            return redirect('EmployeesPage')

    context = {'PersonForm': person_form, 'position_form': position_form,
               'base': base(request), 'getEmployeesTasks': getEmployeesTasks(request)}
    template = 'human_resources/add_employee.html'
    return render(request, template, context)


def EmployeePage(request, pk):
    # Fetch all employee's data from database
    employee = Employee.objects.get(id=pk)
    evaluation = getEvaluation(emp_id=pk)
    # If changing the photo has been requested
    if request.method == 'POST':
        # Get the uploaded image by the user
        img = request.FILES["image_file"]
        # set it for the employee
        q = employee.person
        q.photo = img
        q.save()

    context = {'Employee': employee, 'Evaluation': evaluation,
               'base': base(request), 'getEmployeesTasks': getEmployeesTasks(request)}
    return render(request, 'human_resources/employee.html', context)


def UpdateEmployeePage(request, pk):
    # Getting the employee and person object from database
    employee = Employee.objects.get(id=pk)
    person = Person.objects.get(id=employee.person.id)
    # Setting up the forms
    position_form = EmployeePositionForm(instance=employee)
    person_form = AddPersonForm(instance=person)
    # Check if it is a post method
    if request.method == 'POST':
        person_form = AddPersonForm(request.POST, instance=person)
        position_form = EmployeePositionForm(request.POST, instance=employee)
        # If the forms are valid
        if person_form.is_valid() and position_form.is_valid():
            # Update data
            person_form.save()
            position = position_form['position'].value()
            employee.account.groups.clear()  # delete the employee group
            # assigning the employee with the new position
            Group.objects.get(name=position).user_set.add(employee.account)

            return redirect('EmployeePage', pk)

    context = {'PersonForm': person_form, 'position_form': position_form, 'Employee': employee,
               'base': base(request), 'getEmployeesTasks': getEmployeesTasks(request)}
    template = 'human_resources/update_employee.html'
    return render(request, template, context)


def DeleteEmployeePage(request, pk):
    # Getting the employee object from database
    employee = Employee.objects.get(id=pk)
    # Check if it is a post method
    if request.method == "POST":
        # Delete the employee
        employee.delete()

        return redirect('EmployeesPage')

    context = {'Employee': employee, 'base': base(request),
               'getEmployeesTasks': getEmployeesTasks(request)}
    template = 'human_resources/delete_employee.html'
    return render(request, template, context)


# ------------------------------Distributors------------------------------ #
def DistributorsPage(request):
    # Getting all distributors object from database
    Distributors = Distributor.objects.all()

    context = {'Distributors': Distributors, 'base': base(request),
               'getEmployeesTasks': getEmployeesTasks(request)}
    template = 'human_resources/distributors.html'
    return render(request, template, context)


def AddDistributorPage(request):
    # Setting up the form
    person_form = AddPersonForm()
    # Check if it is a post method
    if request.method == 'POST':
        person_form = AddPersonForm(request.POST)
        # If the form is valid
        if person_form.is_valid():
            # Create person
            person_form.save()
            # Create new distributor and a signal will be sent to run onAddingNewDistributor function in signals.py file
            Distributor.objects.create()

            return redirect('DistributorsPage')

    context = {'PersonForm': person_form, 'base': base(request),
               'getEmployeesTasks': getEmployeesTasks(request)}
    template = 'human_resources/add_distributor.html'
    return render(request, template, context)


def DistributorPage(request, pk):
    # Fetch all distributor's data from database
    distributor = Distributor.objects.get(id=pk)
    # If changing the photo has been requested
    if request.method == 'POST':
        # Get the uploaded image by the user
        img = request.FILES["image_file"]
        # set it for the distributor
        q = distributor.person
        q.photo = img
        q.save()

    context = {'Distributor': distributor, 'base': base(request),
               'getEmployeesTasks': getEmployeesTasks(request)}
    return render(request, 'human_resources/distributor.html', context)


def UpdateDistributorPage(request, pk):
    # Getting the distributor and person object from database
    distributor = Distributor.objects.get(id=pk)
    person = Person.objects.get(id=distributor.person.id)
    # Setting up the form
    person_form = AddPersonForm(instance=person)
    # Check if it is a post method
    if request.method == 'POST':
        person_form = AddPersonForm(request.POST, instance=person)
        # If the form is valid
        if person_form.is_valid():
            # Update data
            person_form.save()

            return redirect('DistributorPage', pk)

    context = {'PersonForm': person_form, 'Distributor': distributor,
               'base': base(request), 'getEmployeesTasks': getEmployeesTasks(request)}
    template = 'human_resources/update_distributor.html'
    return render(request, template, context)


def DeleteDistributorPage(request, pk):
    # Getting the distributor object from database
    distributor = Distributor.objects.get(id=pk)
    # Check if it is a post method
    if request.method == "POST":
        # Delete the distributor
        distributor.delete()

        return redirect('DistributorsPage')

    context = {'Distributor': distributor, 'base': base(request),
               'getEmployeesTasks': getEmployeesTasks(request)}
    template = 'human_resources/delete_distributor.html'
    return render(request, template, context)


# ------------------------------Tasks------------------------------ #
def TasksPage(request):
    # Getting all tasks data from database
    Tasks = Task.objects.all()

    context = {'Tasks': Tasks, 'base': base(request),
               'getEmployeesTasks': getEmployeesTasks(request)}
    template = 'human_resources/tasks.html'
    return render(request, template, context)


def AddTaskPage(request):
    # Setting up the form
    form = AddTaskForm()
    # Check if it is a post method
    if request.method == "POST":
        form = AddTaskForm(request.POST)
        # If the form is valid
        if form.is_valid():
            # Add new task
            form.save()

            return redirect('TasksPage')

    context = {'form': form, 'base': base(request),
               'getEmployeesTasks': getEmployeesTasks(request)}
    template = 'human_resources/add_task.html'
    return render(request, template, context)


def TaskPage(request, pk):
    # Fetch the task's data from database
    task = Task.objects.get(id=pk)
    # Get the task rate if it exist, else set it to None
    try:
        task_rate = TaskRate.objects.get(task=task)
    except TaskRate.DoesNotExist:
        task_rate = None

    context = {'Task': task, 'TaskRate': task_rate, 'base': base(request),
               'getEmployeesTasks': getEmployeesTasks(request)}
    template = 'human_resources/task.html'
    return render(request, template, context)


def UpdateTaskPage(request, pk):
    # Fetch the task's data from database
    task = Task.objects.get(id=pk)
    # Setting up the form
    form = AddTaskForm(instance=task)
    # Check if it is a post method
    if request.method == 'POST':
        form = AddTaskForm(request.POST, instance=task)
        # If the form is valid
        if form.is_valid():
            # Update
            form.save()

            return redirect('TaskPage', pk)

    context = {'form': form, 'TaskID': task.id, 'base': base(request),
               'getEmployeesTasks': getEmployeesTasks(request)}
    template = 'human_resources/update_task.html'
    return render(request, template, context)


def DeleteTaskPage(request, pk):
    # Fetch the task's data from database
    task = Task.objects.get(id=pk)
    # Check if it is a post method
    if request.method == "POST":
        # Delete the task. note: deleteTaskRate function in signals.py will be executed
        task.delete()

        return redirect('TasksPage')

    context = {'Task': task, 'base': base(request),
               'getEmployeesTasks': getEmployeesTasks(request)}
    template = 'human_resources/delete_Task.html'
    return render(request, template, context)


# ------------------------------Evaluation------------------------------ #
def EvaluationPage(request):
    # Get the employees Evaluations
    evaluation = getEvaluation()

    context = {'Evaluation': evaluation, 'base': base(request),
               'getEmployeesTasks': getEmployeesTasks(request)}
    template = 'human_resources/evaluation.html'
    return render(request, template, context)


def WeeklyEvaluationPage(request):
    # Fetch the unrated weeks data from database
    weeks = Week.objects.filter(is_rated=False)

    context = {'week_to_rate_exists': True, 'base': base(
        request), 'getEmployeesTasks': getEmployeesTasks(request)}
    # if there is no unrated weeks, just send a success message
    if not weeks.exists():
        messages.success(request, "Weekly evaluation has been don")
        context['week_to_rate_exists'] = False
    else:
        # Fetch the employees' data from database excluding the HR and CEO
        Employees = Employee.objects.filter(
            ~Q(position="CEO") & ~Q(position="Human Resources"))
        context['Employees'] = Employees
        # if there is more than one unrated weeks
        if len(weeks) > 1:
            unrated_weeks_to_delete = 0
            for index, week in enumerate(weeks):
                # if it is the last week, send the following messages only
                if index == len(weeks) - 1:
                    messages.warning(
                        request, "There are more than one week you have been not rated.")
                    messages.warning(
                        request, f"{unrated_weeks_to_delete} unrated week/s have been deleted from database, only last unrated week left.")
                    messages.info(
                        request, "message have been sent to the CEO regarding this.")
                # else delete the week
                else:
                    week.delete()
                    unrated_weeks_to_delete += 1
        # Check if it is a post method
        if request.method == "POST":
            # get the employees rate from the user and create a weekly rate for each employee
            for emp in Employees:
                val = request.POST.get(f'val{str(emp.id)}', False)
                WeeklyRate.objects.create(
                    week=weeks[0],
                    employee=emp,
                    rate=int(val))
            # change the week state to be already rated
            weeks[0].is_rated = True
            weeks[0].save()

            return redirect('EvaluationPage')

    template = 'human_resources/weekly_rate.html'
    return render(request, template, context)


def TaskEvaluationPage(request):
    Tasks = Task.objects.filter(
        ~Q(status="In-Progress") & ~Q(status="Deadlined"), is_rated=False)
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

        messages.success(request, f"Task has been rated successfully")
    if not Tasks.exists():
        messages.info(request, "There is no more tasks to rate")

    context = {'Tasks': Tasks,  'base': base(
        request), 'getEmployeesTasks': getEmployeesTasks(request)}
    template = 'human_resources/task_evaluation.html'
    return render(request, template, context)
