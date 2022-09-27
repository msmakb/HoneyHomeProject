from django import forms
from django.forms import ModelForm
from main.models import Person
from .models import Employee, Task


class DateInput(forms.DateInput):
    # Adjusting the date input
    input_type = 'date'


class DateTimeInput(forms.DateInput):
    # Adjusting the date input
    input_type = 'datetime-local'


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
            'name': forms.TextInput(
                attrs={
                    'required': True,
                    'class': 'form-control',
                    'placeholder': 'Full Name',
                }
            ),

            'gender': forms.Select(
                attrs={
                    'required': True,
                    'class': 'form-control',
                }
            ),

            'nationality': forms.Select(
                attrs={
                    'required': True,
                    'class': 'form-control',
                }
            ),

            'date_of_birth': DateInput(
                attrs={
                    'required': False,
                    'class': 'form-control',
                    'data-provide': 'datepicker',
                }
            ),

            'address': forms.TextInput(
                attrs={
                    'required': False,
                    'class': 'form-control',
                    'placeholder': 'Address',
                }
            ),

            'contacting_email': forms.EmailInput(
                attrs={
                    'required': True,
                    'class': 'form-control',
                    'placeholder': 'Contacting Email',
                }
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'required': True,
                    'class': 'form-control',
                    'placeholder': '+123 123456789',
                    #  format: '[+][1 to 3 numbers][space][9 to 14 numbers]'
                    'pattern': "[+][0-9]{1,3} [0-9]{9,14}",
                    'type': 'tel',
                }
            ),
        }


class EmployeePositionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(EmployeePositionForm, self).__init__(*args, **kwargs)

        POSITIONS = [
            ('CEO', 'CEO'),
            ('Human Resources', 'Human Resources'),
            ('Warehouse Admin', 'Warehouse Admin'),
            ('Accounting Manager', 'Accounting Manager'),
            ('Social Media Manager', 'Social Media Manager'),
            ('Designer', 'Designer'),
        ]

        employees = Employee.objects.all()
        for employee in employees:
            existingPosition = employee.position
            if 'instance' in kwargs:
                if kwargs['instance'].position == existingPosition:
                    continue

            if (f'{existingPosition}', f'{existingPosition}') in POSITIONS:
                POSITIONS.remove(
                    (f'{existingPosition}', f'{existingPosition}'))

        widget = forms.Select(
            attrs={
                'required': True,
                'class': 'form-control',
            }
        )

        self.fields['position'] = forms.ChoiceField(
            choices=POSITIONS,
            widget=widget
        )
                
    class Meta:
        model = Employee
        fields = ['position', ]


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
            'employee': forms.Select(
                attrs={'required': True, 'class': 'form-control'}
            ),

            'name': forms.TextInput(
                attrs={
                    'required': True,
                    'class': 'form-control',
                    'placeholder': 'Task',
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'required': False,
                    'class': 'form-control',
                    'placeholder': 'Description',
                }
            ),

            'deadline_date': DateTimeInput(
                attrs={
                    'required': False,
                    'class': 'form-control',
                    'data-provide': 'datepicker',
                }
            ),
        }
        
