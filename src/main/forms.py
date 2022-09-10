from django import forms

class LoginForm(forms.Form):
    UserName = forms.CharField(label="User Name", max_length=20)
    Password = forms.CharField(label="Password", max_length=20, widget=forms.PasswordInput())
    