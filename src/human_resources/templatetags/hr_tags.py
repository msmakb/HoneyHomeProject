from django import template
from ..evaluation import allTimeEvaluation


register = template.Library()

@register.simple_tag
def getAllTimeEvaluation(pk):
    return allTimeEvaluation(pk)


@register.simple_tag
def calculateTaskRate(a, b):
    return (a+b) / 2
