from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def index(request):
    return render(request, 'base.html')
def checks(request):
    return render(request, 'checks.html')

def signin_or_login(request):
    if request.method == 'POST':
        action = request.POST.get('action')  # 'login' or 'signup'

        if action == 'signup':
            # Handle Sign Up
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()  # Create new user
                username = form.cleaned_data.get('username')
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