from django import forms

class StudentLoginForm(forms.Form):
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(label = '', widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

class StaffLoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'ID'}))
    password = forms.CharField(label = '', widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

class RegisterForm(forms.Form):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    TYPE_CHOICES = [('Student', 'Student'), ('Coordinator', 'Coordinator'), ('Staff', 'Staff')]
    
    first_name = forms.CharField(max_length=50,label = "Name",)
    last_name = forms.CharField(max_length=50,label = "Surname",)
    email = forms.CharField(max_length="50", label="E-mail",)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Gender", required=True)
    type = forms.ChoiceField(choices=TYPE_CHOICES, label="Type", required=True)
    password = forms.CharField(max_length=20,label = "Password",widget = forms.PasswordInput)
    confirm = forms.CharField(max_length=20,label = "Confirm Password",widget = forms.PasswordInput)

    def clean(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        gender = self.cleaned_data.get("gender")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        type = self.cleaned_data.get("type")
        
        if password and confirm and password != confirm:
            raise forms.ValidationError("Password confirmation does not match.")
        
        values = {
            "first_name" : first_name,
            "last_name" : last_name,
            "gender": gender,
            "email" : email,
            "password" : password,
            "type": type
        }

        return values