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
        fields = ['customer', 'name', 'address', 'contact', 'status', 'inspectors', 'startDT', 'departDT','comments']
        widgets = {
            'inspectors': forms.SelectMultiple(),
            'startDT': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'departDT': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(CheckupForm, self).__init__(*args, **kwargs)
        inspectors_group = Group.objects.get(name='Inspector')
        self.fields['inspectors'].queryset = User.objects.filter(groups=inspectors_group)


class UserUpdateForm(forms.ModelForm):
    
    addresses = forms.CharField(max_length=500, required=False)
    preferences = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        if self.instance:
            customer_profile = CustomerProfile.objects.get(customer=self.instance)
            self.fields['addresses'].initial = customer_profile.addresses
            self.fields['preferences'].initial = customer_profile.preferences

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        if commit:
            user.save()
            customer_profile, created = CustomerProfile.objects.get_or_create(customer=user)
            customer_profile.addresses = self.cleaned_data['addresses']
            customer_profile.preferences = self.cleaned_data['preferences']
            customer_profile.save()
            return user

