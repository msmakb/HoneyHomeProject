from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone

from distributor.models import Distributor
from main.decorators import allowed_users
from main.models import Person
from main.tasks import getEmployeesTasks
from main.utils import getUserBaseTemplate as base

from . import alerts
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
            alerts.employee_added(request)

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
        alerts.employee_photo_updated(request)

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
            alerts.employee_data_updated(request)

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
        alerts.employee_removed(request)

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
            alerts.distributor_added(request)

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
        alerts.distributor_photo_updated(request)

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
            alerts.distributor_data_updated(request)

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
        alerts.distributor_removed(request)

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
            alerts.Task_added(request)

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
            alerts.Task_data_updated(request)

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
        alerts.Task_removed(request)

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
        alerts.evaluation_done(request)
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
                    alerts.many_weeks(request)
                    alerts.deleted_weeks(request, unrated_weeks_to_delete)
                    alerts.inform_ceo(request)
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
            # change the week state
            weeks[0].is_rated = True
            weeks[0].save()

            # change the last weekly evaluations task state
            task = Task.objects.get(name="Evaluate employees", is_rated=False)
            task.status = "On-Time"
            task.submission_date = timezone.now()
            task.is_rated = True
            task.save()
            # Rate the task automatically
            TaskRate.objects.create(task=task, on_time_rate=5, rate=5)

            return redirect('EvaluationPage')

    template = 'human_resources/weekly_rate.html'
    return render(request, template, context)


def TaskEvaluationPage(request):
    # Fetch the submitted tasks data from database
    if request.user.groups.all()[0].name == "Human Resources":
        Tasks = Task.objects.filter(
            ~Q(status="In-Progress") & ~Q(status="Overdue"),
            ~Q(employee__position="Human Resources"), is_rated=False)
    else:
        Tasks = Task.objects.filter(
            ~Q(status="In-Progress") & ~Q(status="Overdue"), is_rated=False)
    # Check if it is a post method
    if request.method == "POST":
        # Get the posted (rated) task id
        id = request.POST.get('id', False)
        # Get the value of the posted task rate
        val = request.POST.get(f'val{str(id)}', False)
        # Fetch the task from database and calculate 'on time rate'
        task = Task.objects.get(id=int(id))
        on_time = 5
        if task.status != "On-Time":
            on_time = 2.5
        # Rate the task
        TaskRate.objects.create(
            task=task, on_time_rate=on_time, rate=float(val))
        task.is_rated = True
        task.save()
        # Get the auto task for the HR and process it
        auto_task = Task.objects.get(
            employee__position="Human Resources",
            description=f"Don't forget to rate {task.employee.person.name}'s submitted task. '{task.name}' Task.",
            is_rated=False)
        on_time = 5
        status = 'On-Time'
        if auto_task.status != 'In-Progress':
            on_time = 2.5
            status = 'Late-Submission'
        TaskRate.objects.create(
            task=auto_task, on_time_rate=on_time, rate=float(5))
        auto_task.status = status
        auto_task.is_rated = True
        auto_task.submission_date = timezone.now()
        auto_task.save()
        print(auto_task.description)
        print(TaskRate.objects.all().order_by('-id')[0])
        # Success message
        alerts.tasks_evaluation_done(request)
    # If there is no tasks to rate just send a message
    if not Tasks.exists():
        alerts.no_tasks_to_rate(request)

    context = {'Tasks': Tasks,  'base': base(request),
               'getEmployeesTasks': getEmployeesTasks(request)}
    template = 'human_resources/task_evaluation.html'
    return render(request, template, context)
