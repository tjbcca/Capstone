from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.shortcuts import *
from django.contrib.auth.forms import UserCreationForm
from app.models import *
from django.contrib.auth.decorators import login_required
from app.forms import *
import random


def home(request):
    context = {'percentage':50}
    return render(request, 'base.html', Context(request,context))

@login_required
def checks(request, checkup_id):
    checkup = get_object_or_404(Checkup, id=checkup_id)
    if request.user != checkup.inspector:
        return redirect('base.html')  # Render a "Forbidden" page if the user is not the inspector

    if request.method == 'POST':
        formset = [ChecklistItemForm(request.POST, prefix=str(item.id), instance=item) for item in checkup.items.all()]
        if all(form.is_valid() for form in formset):
            for form in formset:
                form.save()
            return redirect('checks', checkup_id=checkup.id)
    else:
        formset = [ChecklistItemForm(prefix=str(item.id), instance=item) for item in checkup.items.all()]
    context = {'checkup': checkup, 'formset': formset, 'user': request.user}
    return render(request, 'checks.html', Context(request,context))

def signin_or_login(request):
    if request.method == 'POST':
        action = request.POST.get('action')  # 'login' or 'signup'

        if action == 'signup':
            # Handle Sign Up
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()  # Create new user
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(request, username=username, password=password)
                auth_login(request,user)
                messages.success(request, f'Account created for {username}!')
                return redirect('Home')  # Redirect to landing page after successful sign-up
            else:
                messages.error(request, "Sign Up failed. Please check the form.")
                # Return the form back to the template with errors
                return render(request, 'index.html', {'form': form})

        elif action == 'login':
            # Handle Login
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                #this is for the page it needs to go to after login.
                return redirect('Home')  # Redirect to home page after successful login
            else:
                messages.error(request, 'Invalid username or password.')

    # If the request method is not POST, create an empty form and render the page
    form = UserCreationForm()
    return render(request, 'index.html', {'form': form})

def Logout(request):
    logout(request)
    return redirect('login')