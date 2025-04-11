from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.shortcuts import *
from django.contrib.auth.forms import UserCreationForm
from app.models import *
from django.contrib.auth.decorators import login_required
from app.forms import *
import random
from django.contrib.auth.models import Group
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Q

@login_required
def home(request):
    if (request.user.is_authenticated != True):
        print("You not logged in")
        return redirect('login')
    yourCheckups = Checkup.objects.filter(customer=request.user)
    assignedCheckups = Checkup.objects.filter(inspectors=request.user)
    context = {'assignedChecks':assignedCheckups,'yourChecks':yourCheckups}
    return render(request, 'base.html', Context(request,context))

def is_user_in_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False
    return group in user.groups.all()

@login_required
def checks(request, checkup_id):
    checkup = get_object_or_404(Checkup, id=checkup_id)
    if request.user not in checkup.inspectors.all():
            return redirect('Home')

    if request.method == 'POST':
        formset = [ChecklistItemForm(request.POST, prefix=str(item.id), instance=item) for item in checkup.items.all()]
        if all(form.is_valid() for form in formset):
            for form in formset:
                form.save()
            return redirect('checks', checkup_id=checkup.id)
    else:
        formset = [ChecklistItemForm(prefix=str(item.id), instance=item) for item in checkup.items.all()]
    context = {'checkup': checkup, 'formset': formset,'percentage':checkup.completion_percentage()}
    return render(request, 'checks.html', Context(request,context))

@login_required
def manage(request):
    if not is_user_in_group(request.user, 'Inspector'):
        return redirect('Home')
    query = request.GET.get('q')
    status_filter = request.GET.get('status')
    month_filter = request.GET.get('month')
    year_filter = request.GET.get('year')
    
    checkups = Checkup.objects.all()
    
    if query:
        checkups = checkups.filter(name__icontains=query)
    
    if status_filter:
        checkups = checkups.filter(status=status_filter)
    
    if month_filter and year_filter:
        checkups = checkups.filter(Q(startDT__month=month_filter) & Q(startDT__year=year_filter))
    elif month_filter:
        checkups = checkups.filter(startDT__month=month_filter)
    elif year_filter:
        checkups = checkups.filter(startDT__year=year_filter)
    
    months = range(1, 13)
    years = range(2020, 2100)
    
    context = {
        'checkups': checkups,
        'query': query,
        'status_filter': status_filter,
        'month_filter': month_filter,
        'year_filter': year_filter,
        'months': months,
        'years': years,
    }
    return render(request, 'management.html', Context(request,context))

@login_required
def calendar_view(request):
    year = datetime.now().date().year
    month = datetime.now().date().month
    if is_user_in_group(request.user,'Inspector'):
        checkups = Checkup.objects.filter(startDT__year=year, startDT__month=month)
    else:
        checkups = Checkup.objects.filter(startDT__year=year, startDT__month=month, customer=request.user)
    events = [{'date': checkup.startDT, 'name': checkup.name, 'address':checkup.address,'status':checkup.status,'id':checkup.id} for checkup in checkups]

    # Generate calendar structure
    calendar = generate_calendar(year, month)

    context = {
        'month': month,
        'year': year,
        'calendar': calendar,
        'events': events,
    }
    return render(request, 'calendar.html', Context(request,context))

def generate_calendar(year, month):
    # Function to generate calendar structure
    import calendar
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)
    return month_days

def signin_or_login(request):
    if request.user.is_authenticated:
        print("You are already logged in")
        return redirect('Home')
    if request.method == 'POST':
        action = request.POST.get('action')  # 'login' or 'signup'

        if action == 'signup':
            # Handle Sign Up
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)  # Create new user without saving to the database yet
                email = request.POST.get('email')  # Get email from POST data
                user.email = email  # Set the email for the user
                user.save()  # Save the user with the email
                CustomerProfile.objects.create(customer=user)
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(request, username=username, password=password)
                auth_login(request, user)
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

@login_required
def checkupCreate(request, checkup_id=None):
    if checkup_id:
        checkup = get_object_or_404(Checkup, id=checkup_id)
        if (request.user==checkup.customer) and (request.user not in checkup.inspectors.all()):
            context = {'checkup': checkup,'percentage':checkup.completion_percentage()}
            return render(request, 'customerView.html', Context(request,context))
        else:
            if request.user not in checkup.inspectors.all():
                return redirect('Home')  # Redirect to a permission denied page or another page
    else:
        checkup = None
    if not is_user_in_group(request.user, 'Inspector'):
        return redirect('Home')
    if request.method == 'POST':
        if 'delete' in request.POST:
            checkup.delete()
            return redirect('management')  # Redirect to a list view after deletion
        else:
            form = CheckupForm(request.POST, instance=checkup)
            if form.is_valid():
                form.save()
                return redirect('management')  # Redirect to a list view or detail view after saving
    else:
        form = CheckupForm(instance=checkup)

    context = {
        'form': form,
        'checkup': checkup,
    }
    return render(request, 'create.html', Context(request,context))

@login_required
def update_user(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('userProfile')  # Redirect to a profile page or another page
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'update_user.html', Context(request, {'form': form}))

@login_required
def accounts(request):
    if not is_user_in_group(request.user, 'Inspector'):
        return redirect('Home')
    query = request.GET.get('q', '')  # Get the search query from the GET request
    status_filter = request.GET.get('status')
    users = User.objects.all()  # Start with all users

    # If there's a query, filter users by username, email, or first name
    if query:
        # Use Q objects to filter by multiple fields (OR logic)
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query)
        )

    if status_filter and status_filter != 'All':
        for user in users:
            if user.groups.filter(name="Inspector").exists():
                print(user.username)
        if status_filter  and status_filter == "Worker":
             users = users.filter(groups__name="Inspector")

        elif status_filter and status_filter == "Customer":
            users = users.exclude(groups__name="Inspector")
    

    context = {
        'users': users,
        'query': query  # This will pass the search query back to the template
    }

    return render(request, 'accountview.html', Context(request, context))

@login_required
def manageUser(request, user_id):
    if not is_user_in_group(request.user, 'Inspector'):
        return redirect('Home')
    user = get_object_or_404(User, id=user_id)
    edit_mode = is_user_in_group(request.user, 'Admin')

    checkups = Checkup.objects.filter(customer=user).order_by('startDT').reverse()

    if request.method == 'POST' and edit_mode:
        form = AdminUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            context = {
                'account': user,
                'form': form,
                'checkups': checkups,
                'edit_mode': edit_mode,
            }
            return render(request, 'UserEdit.html', Context(request, context))
    else:
        form = AdminUserUpdateForm(instance=user)

    context = {
        'account': user,
        'form': form,
        'checkups': checkups,
        'edit_mode': edit_mode,
        'customer_profile': CustomerProfile.objects.get(customer=user)
    }
    if edit_mode:
        return render(request, 'UserEdit.html', Context(request, context))
    else:
        return render(request, 'UserInfo.html', Context(request, context))

@login_required
def history(request):
    context = {
        'checkups': Checkup.objects.filter(customer=request.user).order_by('startDT').reverse()
    }
    return render(request, 'history.html', Context(request,context))