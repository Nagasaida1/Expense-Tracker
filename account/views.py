from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from income.models import Income
from django.db import models
from expense.models import Expense
from .forms import LoginForm, UserForm, UserForm1,ProfileForm  # Ensure these forms are defined in `forms.py`

# Home Page
def home1(request):
    context = {
        'bal': get_balance(request),
        'incb': get_income(request),
        'expb': get_expense(request),
    }
    return render(request, 'home.html', context)

# Registration




def reg1(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user form
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Create the profile object (but don't save it yet)
            profile = profile_form.save(commit=False)
            profile.user = user  # Link the profile to the newly created user
            profile.save()  # Save the profile to the database

            # Redirect to login page after successful registration
            return redirect('/login')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request, 'form.html', {'user_form': user_form, 'profile_form': profile_form})

# Login
def login12(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['uid'] = user.id  # Save user ID in session
            return redirect('/')
        else:
            error = "Invalid username or password."
            form = LoginForm()
            return render(request, 'login.html', {'d': form, 'error': error})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'d': form})

# Logout
def logout12(request):
    logout(request)
    request.session.flush()  # Clear session data
    return redirect('/')

# Helper Functions
def get_balance(request):
    uid = request.session.get('uid')
    if uid is None:
        return 0  # Default if no user is logged in
    total_income = Income.objects.filter(user_id=uid).aggregate(total=models.Sum('income'))['total'] or 0
    total_expense = Expense.objects.filter(user_id=uid).aggregate(total=models.Sum('expense'))['total'] or 0
    return total_income - total_expense

def get_income(request):
    uid = request.session.get('uid')
    if uid is None:
        return 0
    return Income.objects.filter(user_id=uid).aggregate(total=models.Sum('income'))['total'] or 0

def get_expense(request):
    uid = request.session.get('uid')
    if uid is None:
        return 0
    return Expense.objects.filter(user_id=uid).aggregate(total=models.Sum('expense'))['total'] or 0

# Edit User Profile
def edit1(request):
    uid = request.session.get('uid')
    if uid is None:
        return redirect('/login')  # Redirect to login if user is not logged in
    user = User.objects.get(id=uid)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserForm(instance=user)
    return render(request, 'updateuser.html', {'edit2': form})

# Change Username
def change_name(request):
    uid = request.session.get('uid')
    if uid is None:
        return redirect('/login')
    user = User.objects.get(id=uid)
    if request.method == 'POST':
        form = UserForm1(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserForm1(instance=user)
    return render(request, 'upusername.html', {'edit3': form})

# About Page
def about1(request):
    return render(request, 'about.html')
