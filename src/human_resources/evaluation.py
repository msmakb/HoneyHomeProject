from .models import Employee, Task, TaskRate, Week, WeeklyRate


def newEmployee(emp_id:int) -> bool:
    """
    This function checks if the Employee is new 
    by checking if there is any weekly rate existed
    it will return False if there are any rates found

    Args:
        emp_id (int): Employee ID

    Returns:
        bool: True if the employee is new else False
    """
    if not WeeklyRate.objects.filter(employee=emp_id).exists():
        return True
    return False


def monthlyRate(emp_id:int) -> float:
    """
    This function will return the monthly rate of the employee 
    by calculating the last 4 weeks' rates, 
    if the employee has not been weekly rated the function will return 0

    Args:
        emp_id (int): Employee ID

    Returns:
        float: Monthly rate
    """
    if not newEmployee(emp_id):
        rate, count = 0, 0
        emp_weekly_rates = WeeklyRate.objects.filter(employee=emp_id).order_by('-id')
        for i in emp_weekly_rates:
            if count == 4:
                break
            rate += i.rate
            count += 1

        return 0 if count == 0 else round((rate/count), 2)

    return 0


def monthlyTaskRate(emp_id:int) -> float:
    """
    This function will return the monthly task rate of the employee 
    by calculating the last 4 weeks' task rates, 
    if the employee has no tasks or his tasks is not rated the function will return 0

    Args:
        emp_id (int): Employee ID

    Returns:
        float: Monthly task rate
    """
    if not newEmployee(emp_id):
        from django.utils import timezone
        from datetime import timedelta
        
        rate, count = 0, 0
        today = timezone.now()
        end_date = today - timedelta(days=30)
        empTasks = Task.objects.filter(employee=emp_id, 
                                        receiving_date__range=[end_date, today]) 
        if empTasks.exists():
            for task in empTasks:
                task_rate = TaskRate.objects.filter(task=task)
                if task_rate.exists():
                    task_rate = task_rate[0]
                    rate += task_rate.rate
                    rate += task_rate.on_time_rate
                    count += 1
            if count != 0: 
                return round(((rate/count) /2), 2)
                
    return 0


def weeklyRate(week_id:int, emp_id:int) -> float:
    """
    This function will return the last week rate of the employee 
    if the employee has not been weekly rated ever the function will return 0

    Args:
        last_week_id (int): ID of the las week
        emp_id (int): Employee ID

    Returns:
        float: Employee weekly rate
    """
    if not newEmployee(emp_id):
        if week_id != -1:
            return WeeklyRate.objects.get(week__id=week_id, employee=emp_id).rate

    return 0


def monthlyOverallEvaluation(emp_id:int) -> float:
    """
    This function calculating the monthly overall evaluation

    Args:
        em_id (int): Employee ID

    Returns:
        float: Monthly overall evaluation
    """
    if not newEmployee(emp_id):
        return round(((monthlyRate(emp_id) + monthlyTaskRate(emp_id)) / 2), 2)

    return 0


def allTimeEvaluation(emp_id:int) -> float:
    """
    This function calculating all time evaluation for the employee
    Args:
        emp_id (int): Employee ID

    Returns:
        float: All time evaluation
    """
    if not newEmployee(emp_id):
        # All Time Weekly Rate
        rate, count = 0, 0
        emp_weekly_rates = WeeklyRate.objects.filter(employee=emp_id)
        if emp_weekly_rates.exists():
            for weekly_rate in emp_weekly_rates:
                rate += weekly_rate.rate
                count += 1
        all_time_weekly_rate = 0 if count == 0 else rate/count
        del rate, count

        # All Tasks Rate
        rate, count = 0, 0
        empTasks = Task.objects.filter(employee=emp_id)
        if empTasks.exists():
            for task in empTasks: 
                task_rate = TaskRate.objects.filter(task=task)
                if task_rate.exists():
                    task_rate = task_rate[0]
                    rate += task_rate.rate
                    rate += task_rate.on_time_rate
                    count += 1
        all_task_rate = 0 if count == 0 else (rate/count) /2
        return round(((all_time_weekly_rate + all_task_rate) / 2), 2)

    return 0


def getEvaluation(emp_id=-1) -> dict:
    """
    This function if employee id not specified it will return all employees' evaluations 
    else it will return the evaluation of the specified employee's evaluations

    Args:
        emp_id (int, optional): Employee ID. Defaults to -1.

    Returns:
        dict: Employee/s evaluation
    """
    evaluation = {}
    if emp_id != -1: # if the employee specified
        employee = Employee.objects.get(id=emp_id)
        evaluation = {'Employee':employee, 
                        'MonthlyRate':monthlyRate(emp_id),
                        'WeeklyRate':weeklyRate(Week.getLastWeekID(), emp_id),
                        'MonthlyTaskRate':monthlyTaskRate(emp_id),
                        'MonthlyOverallEvaluation':monthlyOverallEvaluation(emp_id),
                        'AllTimeEvaluation':allTimeEvaluation(emp_id),
                        }
    else:
        for employee in Employee.objects.all():
            emp_id = employee.id
            evaluation[employee.person.name] = {'Employee':employee, 
                                                'MonthlyRate':monthlyRate(emp_id),
                                                'WeeklyRate':weeklyRate(Week.getLastWeekID(), emp_id),
                                                'MonthlyTaskRate':monthlyTaskRate(emp_id),
                                                'MonthlyOverallEvaluation':monthlyOverallEvaluation(emp_id),
                                                'AllTimeEvaluation':allTimeEvaluation(emp_id)
                                                }

    return evaluation
