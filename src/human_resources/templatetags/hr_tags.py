from django import template
from human_resources.Evaluation import Evaluation
from main.models import Employee, Task, TaskRate, Week, WeeklyRate


register = template.Library()
@register.simple_tag
def getAllTimeEvaluation(pk):
    return Evaluation(Employee, Task, TaskRate, Week, WeeklyRate).evaluation(emp_id=pk).get('AllTimeEvaluation')

