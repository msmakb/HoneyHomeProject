from django.db.models import Q


class Evaluation:
    
    def __init__(self, Employee, Task, TaskRate, Week, WeeklyRate) -> None:
        self.Employee = Employee
        self.Task = Task
        self.TaskRate = TaskRate
        self.Week = Week
        self.WeeklyRate = WeeklyRate

    def evaluation(self, emp_id='all'): 
        new_employee = False
        last_week = self.Week.objects.filter(is_rated=True).order_by('-id')[0]
        Employees = self.Employee.objects.filter(~Q(position="CEO") & ~Q(position="Human Resources"))
        Evaluation = {}
        for employee in Employees:
            if emp_id != 'all':
                if employee.id != int(emp_id):
                    continue
            if not self.WeeklyRate.objects.filter(employee=employee).exists():
                new_employee = True
            if not new_employee:
                # Monthly Rate
                temp, count = 0, 0
                empWeeklyRates = self.WeeklyRate.objects.filter(employee=employee).order_by('-id')
                for i in empWeeklyRates:
                    if count == 4:
                        break
                    temp += i.rate
                    count += 1
                try:
                    MonthlyRate = temp/count
                except ZeroDivisionError: pass
                temp, count = 0, 0
                # Monthly Tasks Rate
                from datetime import date, timedelta
                today = date.today() + timedelta(days=1)
                enddate = today - timedelta(days=30)
                MonthlyTaskRate = 5.0
                try:
                    empTasks = self.Task.objects.filter(employee=employee, 
                                                receiving_date__range=[enddate, today])            
                    for i in empTasks: 
                        temp += self.TaskRate.objects.get(task=i).rate
                        temp += self.TaskRate.objects.get(task=i).on_time_rate
                        count += 1
                    if count != 0: 
                        MonthlyTaskRate = (temp/count) /2
                except (self.Task.DoesNotExist, self.TaskRate.DoesNotExist): pass
                # Weekly Rate
                empWeeklyRates = self.WeeklyRate.objects.filter(week=last_week, employee=employee)[0].rate
                # Monthly Overall Evaluation
                monthlyOverallEvaluation = (MonthlyRate + MonthlyTaskRate) / 2
                # All Time Evaluation
                temp, count = 0, 0
                for i in self.WeeklyRate.objects.filter(employee=employee):
                    temp += i.rate
                    count += 1
                AllTimeWeeklyRate = temp/count
                temp, count = 0, 0
                AllTaskRate = 5.0
                try:
                    empTasks = self.Task.objects.filter(employee=employee)
                    for i in empTasks: 
                        temp += self.TaskRate.objects.get(task=i).rate
                        temp += self.TaskRate.objects.get(task=i).on_time_rate
                        count += 1
                    if count != 0: 
                        AllTaskRate = (temp/count) /2
                except (self.Task.DoesNotExist, self.TaskRate.DoesNotExist): pass
                AllTimeEvaluation = (AllTimeWeeklyRate + AllTaskRate) / 2
                Evaluation[employee.person.name] = {'Employee':employee, 
                                                    'MonthlyRate':MonthlyRate,
                                                    'WeeklyRate':empWeeklyRates,
                                                    'MonthlyTaskRate':MonthlyTaskRate,
                                                    'MonthlyOverallEvaluation':monthlyOverallEvaluation,
                                                    'AllTimeEvaluation':AllTimeEvaluation
                                                    }
                if emp_id != 'all': 
                    if employee.id == int(emp_id):
                        Evaluation = {'Employee':employee, 
                                        'MonthlyRate':MonthlyRate,
                                        'WeeklyRate':empWeeklyRates,
                                        'MonthlyTaskRate':MonthlyTaskRate,
                                        'MonthlyOverallEvaluation':monthlyOverallEvaluation,
                                        'AllTimeEvaluation':AllTimeEvaluation,
                                        }
                        break
            else:
                Evaluation[employee.person.name] = {'Employee':employee, 
                                                'MonthlyRate':0,
                                                'WeeklyRate':0,
                                                'MonthlyTaskRate':0,
                                                'MonthlyOverallEvaluation':0,
                                                'AllTimeEvaluation':0,
                                                }
                new_employee = False

        return Evaluation
    