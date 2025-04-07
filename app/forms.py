from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.contrib.auth.models import User, Group
from app.models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ['description', 'is_completed']
        widgets = {
            'description': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

class CheckupForm(forms.ModelForm):
    class Meta:
        model = Checkup
        fields = ['customer', 'name', 'address', 'contact', 'status', 'inspectors', 'startDT', 'departDT']
        widgets = {
            'inspectors': forms.SelectMultiple(),
            'startDT': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'departDT': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(CheckupForm, self).__init__(*args, **kwargs)
        inspectors_group = Group.objects.get(name='Inspector')
        self.fields['inspectors'].queryset = User.objects.filter(groups=inspectors_group)