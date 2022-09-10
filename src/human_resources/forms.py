from django import forms
from django.forms import ModelForm
from main.models import Person, Employee, Task

class DateInput(forms.DateInput):
    input_type = 'date'

class AddPersonForm(ModelForm):
    class Meta:
        model = Person
        fields = [
            'name',
            'gender',
            'nationality',
            'date_of_birth',
            'address',
            'contacting_email',
            'phone_number',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Full Name'}),
            'gender': forms.Select(attrs={'required': True, 'class': 'form-control'}),
            'nationality': forms.Select(attrs={'required': True, 'class': 'form-control'}),
            'date_of_birth': DateInput(attrs={'required': False, 'class': 'form-control', 'data-provide':'datepicker'}),
            'address': forms.TextInput(attrs={'required': False, 'class': 'form-control','placeholder': 'Address'}),
            'contacting_email': forms.EmailInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Contacting Email'}),
            'phone_number': forms.TextInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Phone number'}),
        }

class GetEmployeePosition(ModelForm):
    class Meta:
        model = Employee
        fields = ['position']
        widgets = {'position': forms.Select(attrs={'required': True, 'class': 'form-control'})}

class AddTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            'employee',
            'name',
            'description',
            'deadline_date',
        ]
        widgets = {
            'employee': forms.Select(attrs={'required': True, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Task'}),
            'description': forms.Textarea(attrs={'required': False, 'class': 'form-control', 'placeholder': 'Description'}),
            'deadline_date': DateInput(attrs={'required': False, 'class': 'form-control', 'data-provide':'datepicker'}),
        }

class WeeklyRateForm(ModelForm):
    pass