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

    def clean_phone_number(self) -> str:
        """
        This function to validate the phone number inserted with the following format:
        Format: '[+][1 to 3 numbers][space][9 to 14 numbers]'.
        The pattern format is not secure enough to be the only validator.

        Raises:
            forms.ValidationError: The phone number must be started with '+'.
            forms.ValidationError: Only '+' sing in the begging and digits are acceptable.
            forms.ValidationError: There must be a space ' ' between the country key and the phone number.
            forms.ValidationError: The country key must be between 1-3 digits.
            forms.ValidationError: The phone number must be between 9-14 digits.

        Returns:
            str: A valid format for phon number
        """
        phone_number = self.cleaned_data.get('phone_number')
        splitted = phone_number.split(' ')
        # '+' sign in the begging
        if phone_number[0] != '+':
            raise forms.ValidationError(
                "The phone number must be started with '+'.")
        # Check is all digit except the fires index which should be '+'
        try:
            int(splitted[0][1:])
            int(splitted[1])
        except:
            raise forms.ValidationError(
                "Only '+' sing in the begging and digits are acceptable.")
        # Check if there is a space between key and number
        if len(splitted) != 2:
            raise forms.ValidationError(
                "There must be a space ' ' between the country key and the phone number.")
        # Check if the country key is between 1-3 digits
        if len(splitted[0]) > 4 or len(splitted[0]) < 2:
            raise forms.ValidationError(
                "The country key must be between 1-3 digits.")
        # Check if the phone number is between 9-14 digits
        if len(splitted[1]) < 9 or len(splitted[1]) > 14:
            raise forms.ValidationError(
                "The phone number must be between 9-14 digits.")

        return phone_number


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
