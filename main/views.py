from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from main.models import User, UserOnboardingData


@login_required
def home(request):
    if not request.user.survey_filled:
        return redirect('/takeSurvey')

    return render(request, 'dashboard.html')


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
    if request.method == 'POST':
        user = request.user

        income_goal = request.POST.get('step1')
        projects_per_month = request.POST.get('step2')
        average_rate = request.POST.get('step3')
        hours_per_week = request.POST.get('step4')
        primary_industry = request.POST.get('step5')

        _, created = UserOnboardingData.objects.update_or_create(
            user=request.user,
            defaults={
                'income_goal': income_goal,
                'projects_per_month': projects_per_month,
                'average_rate': average_rate,
                'hours_per_week': hours_per_week,
                'primary_industry': primary_industry
            }
        )
        user.survey_filled = True
        user.save()
        return redirect('/')

    return render(request, 'survey.html')


def dashboard(request):
    return render(request, 'dashboard.html')
