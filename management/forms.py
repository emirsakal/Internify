from django import forms

class StudentLoginForm(forms.Form):
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(label = '', widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

class StaffLoginForm(forms.Form):
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(label = '', widget=forms.PasswordInput(attrs={'placeholder':'Password'}))