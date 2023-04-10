from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='ID', widget=forms.TextInput(attrs={'placeholder':'ID'}))
    password = forms.CharField(label = 'Password', widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

class RegisterForm(forms.Form):
    PROFESSION_CHOICES = [('Student','Student'),('Teacher','Teacher'),('CareerCenter','CareerCenter')]
    CLASS_CHOICES = [('Non-Student','Non-Student'),('1.Class','1.Class'),('2.Class','2.Class'),('3.Class','3.Class'),('4.Class', '4.Class')]
    firstName = forms.CharField(max_length=50,label = "Name",)
    lastName = forms.CharField(max_length=50,label = "Surname",)
    profession = forms.ChoiceField(choices=PROFESSION_CHOICES, label="Profession")
    classes = forms.ChoiceField(choices=CLASS_CHOICES, label="Class")
    schoolID = forms.CharField(max_length=9, label = "School ID",)
    email = forms.CharField(max_length="50", label="E-mail",)
    password = forms.CharField(max_length=20,label = "Password",widget = forms.PasswordInput)
    confirm = forms.CharField(max_length=20,label = "Confirm Password",widget = forms.PasswordInput)

    def clean(self):
        firstName = self.cleaned_data.get("firstName")
        lastName = self.cleaned_data.get("lastName")
        profession = self.cleaned_data.get("profession")
        classes = self.cleaned_data.get("classes")
        schoolID = self.cleaned_data.get("schoolID")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Password confirmation does not match.")
        
        values = {
            "firstName" : firstName,
            "lastName" : lastName,
            "profession" : profession,
            "classes" : classes,
            "schoolID" : schoolID,
            "email" : email,
            "password" : password,
        }

        return values