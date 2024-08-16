from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from main.models import User


@login_required
def home(request):
    if not request.user.survey_filled:
        return redirect('/takeSurvey')

    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            print('here')
            login(request, user)
            return redirect('/')
        else:
            print('here')
            messages.error(request, 'Invalid email or password.', extra_tags='danger')

    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already in use.', extra_tags='danger')
                return render(request, 'signup.html')

            user = User.objects.create_user(
                name=name,
                username=email,
                email=email,
                password=password
            )
            user.save()

            login(request, user)
            return redirect('/')
    return render(request, 'signup.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('/login')


def take_survey(request):
    return None