from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum, Q, Avg
from django.utils import timezone
from datetime import datetime, date
from decimal import Decimal

from main.models import User, Client, Project, Payment, MonthlyGoal


@login_required
def home(request):
    return redirect('/dashboard')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid email or password.', extra_tags='danger')

    return render(request, 'login.html')


def signup_view(request):
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


@login_required
def dashboard(request):
    current_month = timezone.now().month
    current_year = timezone.now().year
    
    # Get current month's goal
    try:
        current_goal = MonthlyGoal.objects.get(user=request.user, year=current_year, month=current_month)
    except MonthlyGoal.DoesNotExist:
        current_goal = None
    
    # Get current month's payments
    current_month_payments = Payment.objects.filter(
        project__user=request.user,
        actual_date__year=current_year,
        actual_date__month=current_month,
        status='received'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    # Get last month's payments for comparison
    last_month = current_month - 1 if current_month > 1 else 12
    last_month_year = current_year if current_month > 1 else current_year - 1
    
    last_month_payments = Payment.objects.filter(
        project__user=request.user,
        actual_date__year=last_month_year,
        actual_date__month=last_month,
        status='received'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    # Calculate percentage change
    if last_month_payments > 0:
        payment_percentage = ((current_month_payments - last_month_payments) / last_month_payments) * 100
    else:
        payment_percentage = 100 if current_month_payments > 0 else 0
    
    # Get pending payments for current month
    pending_payments = Payment.objects.filter(
        project__user=request.user,
        expected_date__year=current_year,
        expected_date__month=current_month,
        status='pending'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    # Get overdue payments
    overdue_payments = Payment.objects.filter(
        project__user=request.user,
        status='pending',
        expected_date__lt=timezone.now().date()
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    # Get upcoming payments (next 30 days)
    upcoming_payments = Payment.objects.filter(
        project__user=request.user,
        status='pending',
        expected_date__gte=timezone.now().date(),
        expected_date__lte=timezone.now().date() + timezone.timedelta(days=30)
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    # Get project statistics for chart
    total_projects = Project.objects.filter(user=request.user).count()
    active_projects = Project.objects.filter(user=request.user, status='in_progress').count()
    completed_projects = Project.objects.filter(user=request.user, status='completed').count()
    proposal_projects = Project.objects.filter(user=request.user, status='proposal').count()
    
    # Get last month's project stats for comparison
    last_month_projects = Project.objects.filter(
        user=request.user,
        created_at__year=last_month_year,
        created_at__month=last_month
    ).count()
    
    if last_month_projects > 0:
        project_percentage = ((total_projects - last_month_projects) / last_month_projects) * 100
    else:
        project_percentage = 100 if total_projects > 0 else 0
    
    # Debug: Print project statuses
    print(f"DEBUG: User {request.user.username} has {total_projects} projects:")
    for project in Project.objects.filter(user=request.user):
        print(f"  - {project.name}: {project.status}")
    
    # Get recent payments
    recent_payments = Payment.objects.filter(project__user=request.user).order_by('-actual_date')[:5]
    
    # Get payment pipeline data for chart (last 6 months)
    pipeline_data = []
    for i in range(6):  # Only 6 months historical data
        month_date = timezone.now().date().replace(day=1) - timezone.timedelta(days=30*i)
        month_payments = Payment.objects.filter(
            project__user=request.user,
            actual_date__year=month_date.year,
            actual_date__month=month_date.month,
            status='received'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        pipeline_data.append({
            'month': month_date.strftime('%b %Y'),
            'amount': float(month_payments)
        })
    
    pipeline_data.reverse()
    
    # Always provide chart data, even if empty
    if not pipeline_data:
        pipeline_data = [
            {'month': 'Jan 2024', 'amount': 0},
            {'month': 'Feb 2024', 'amount': 0},
            {'month': 'Mar 2024', 'amount': 0},
            {'month': 'Apr 2024', 'amount': 0},
            {'month': 'May 2024', 'amount': 0},
            {'month': 'Jun 2024', 'amount': 0},
        ]
    
    # Get revenue vs growth data (last 6 months)
    revenue_growth_data = []
    for i in range(6):
        month_date = timezone.now().date().replace(day=1) - timezone.timedelta(days=30*i)
        
        # Actual revenue
        actual_revenue = Payment.objects.filter(
            project__user=request.user,
            actual_date__year=month_date.year,
            actual_date__month=month_date.month,
            status='received'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        # Monthly goal (if exists)
        try:
            monthly_goal = MonthlyGoal.objects.get(
                user=request.user, 
                year=month_date.year, 
                month=month_date.month
            )
            target_revenue = monthly_goal.income_goal
        except MonthlyGoal.DoesNotExist:
            # Estimate goal based on 10% growth from previous month
            if i == 0:  # Current month
                target_revenue = current_goal.income_goal if current_goal else Decimal('50000')
            else:
                # Simple growth estimation
                target_revenue = Decimal('50000') * (Decimal('1.1') ** (5 - i))
        
        revenue_growth_data.append({
            'month': month_date.strftime('%b %Y'),
            'actual': float(actual_revenue),
            'target': float(target_revenue)
        })
    
    revenue_growth_data.reverse()
    
    context = {
        'current_goal': current_goal,
        'current_month_payments': current_month_payments,
        'pending_payments': pending_payments,
        'overdue_payments': overdue_payments,
        'upcoming_payments': upcoming_payments,
        'total_projects': total_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'proposal_projects': proposal_projects,
        'recent_payments': recent_payments,
        'pipeline_data': pipeline_data,
        'revenue_growth_data': revenue_growth_data,
        'payment_percentage': round(payment_percentage, 1),
        'project_percentage': round(project_percentage, 1),
    }
    
    return render(request, 'dashboard.html', context)


# Client Management Views
@login_required
def client_list(request):
    clients = Client.objects.filter(user=request.user)
    
    # Calculate total revenue for each client
    for client in clients:
        total_revenue = client.projects.aggregate(total=Sum('takeaway_amount'))['total'] or Decimal('0')
        client.total_revenue = total_revenue
    
    return render(request, 'clients/list.html', {'clients': clients})


@login_required
def client_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        notes = request.POST.get('notes')
        
        client = Client.objects.create(
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            notes=notes
        )
        messages.success(request, f'Client "{client.name}" created successfully.')
        return redirect('client_list')
    
    return render(request, 'clients/create.html')


@login_required
def client_edit(request, client_id):
    client = get_object_or_404(Client, id=client_id, user=request.user)
    
    if request.method == 'POST':
        client.name = request.POST.get('name')
        client.email = request.POST.get('email')
        client.phone = request.POST.get('phone')
        client.notes = request.POST.get('notes')
        client.save()
        
        messages.success(request, f'Client "{client.name}" updated successfully.')
        return redirect('client_list')
    
    return render(request, 'clients/edit.html', {'client': client})


@login_required
def client_delete(request, client_id):
    client = get_object_or_404(Client, id=client_id, user=request.user)
    client_name = client.name
    client.delete()
    messages.success(request, f'Client "{client_name}" deleted successfully.')
    return redirect('client_list')


# Project Management Views
@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user).select_related('client')
    return render(request, 'projects/list.html', {'projects': projects})


@login_required
def project_create(request):
    if request.method == 'POST':
        client_id = request.POST.get('client')
        name = request.POST.get('name')
        description = request.POST.get('description')
        project_type = request.POST.get('project_type')
        status = request.POST.get('status')
        total_amount = request.POST.get('total_amount')
        takeaway_amount = request.POST.get('takeaway_amount')
        costs = request.POST.get('costs', 0)
        start_date = request.POST.get('start_date')
        completion_date = request.POST.get('completion_date') or None
        
        client = get_object_or_404(Client, id=client_id, user=request.user)
        
        project = Project.objects.create(
            user=request.user,
            client=client,
            name=name,
            description=description,
            project_type=project_type,
            status=status,
            total_amount=total_amount,
            takeaway_amount=takeaway_amount,
            costs=costs,
            start_date=start_date,
            completion_date=completion_date
        )
        
        messages.success(request, f'Project "{project.name}" created successfully.')
        return redirect('project_list')
    
    clients = Client.objects.filter(user=request.user)
    return render(request, 'projects/create.html', {'clients': clients})


@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    
    if request.method == 'POST':
        project.client_id = request.POST.get('client')
        project.name = request.POST.get('name')
        project.description = request.POST.get('description')
        project.project_type = request.POST.get('project_type')
        project.status = request.POST.get('status')
        project.total_amount = request.POST.get('total_amount')
        project.takeaway_amount = request.POST.get('takeaway_amount')
        project.costs = request.POST.get('costs', 0)
        project.start_date = request.POST.get('start_date')
        project.completion_date = request.POST.get('completion_date') or None
        project.save()
        
        messages.success(request, f'Project "{project.name}" updated successfully.')
        return redirect('project_list')
    
    clients = Client.objects.filter(user=request.user)
    return render(request, 'projects/edit.html', {'project': project, 'clients': clients})


@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    project_name = project.name
    project.delete()
    messages.success(request, f'Project "{project_name}" deleted successfully.')
    return redirect('project_list')


# Payment Management Views
@login_required
def payment_list(request):
    payments = Payment.objects.filter(project__user=request.user).select_related('project', 'project__client')
    return render(request, 'payments/list.html', {'payments': payments})


@login_required
def payment_create(request):
    if request.method == 'POST':
        project_id = request.POST.get('project')
        amount = request.POST.get('amount')
        expected_date = request.POST.get('expected_date')
        actual_date = request.POST.get('actual_date') or None
        status = request.POST.get('status')
        notes = request.POST.get('notes')
        
        project = get_object_or_404(Project, id=project_id, user=request.user)
        
        payment = Payment.objects.create(
            project=project,
            amount=amount,
            expected_date=expected_date,
            actual_date=actual_date,
            status=status,
            notes=notes
        )
        
        messages.success(request, f'Payment for "{project.name}" created successfully.')
        return redirect('payment_list')
    
    projects = Project.objects.filter(user=request.user).select_related('client')
    return render(request, 'payments/create.html', {'projects': projects})


@login_required
def payment_edit(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, project__user=request.user)
    
    if request.method == 'POST':
        payment.project_id = request.POST.get('project')
        payment.amount = request.POST.get('amount')
        payment.expected_date = request.POST.get('expected_date')
        payment.actual_date = request.POST.get('actual_date') or None
        payment.status = request.POST.get('status')
        payment.notes = request.POST.get('notes')
        payment.save()
        
        messages.success(request, f'Payment updated successfully.')
        return redirect('payment_list')
    
    projects = Project.objects.filter(user=request.user).select_related('client')
    return render(request, 'payments/edit.html', {'payment': payment, 'projects': projects})


@login_required
def payment_delete(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, project__user=request.user)
    payment.delete()
    messages.success(request, 'Payment deleted successfully.')
    return redirect('payment_list')





# Monthly Goals Views
@login_required
def goal_list(request):
    goals = MonthlyGoal.objects.filter(user=request.user)
    
    # Calculate actual income for each goal
    for goal in goals:
        actual_income = Payment.objects.filter(
            project__user=request.user,
            actual_date__year=goal.year,
            actual_date__month=goal.month,
            status='received'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        goal.actual_income = actual_income
    
    return render(request, 'goals/list.html', {'goals': goals})


@login_required
def goal_create(request):
    if request.method == 'POST':
        year = request.POST.get('year')
        month = request.POST.get('month')
        income_goal = request.POST.get('income_goal')
        
        goal, created = MonthlyGoal.objects.update_or_create(
            user=request.user,
            year=year,
            month=month,
            defaults={'income_goal': income_goal}
        )
        
        if created:
            messages.success(request, f'Goal for {month}/{year} created successfully.')
        else:
            messages.success(request, f'Goal for {month}/{year} updated successfully.')
        
        return redirect('goal_list')
    
    return render(request, 'goals/create.html')


@login_required
def goal_edit(request, goal_id):
    goal = get_object_or_404(MonthlyGoal, id=goal_id, user=request.user)
    
    if request.method == 'POST':
        goal.year = request.POST.get('year')
        goal.month = request.POST.get('month')
        goal.income_goal = request.POST.get('income_goal')
        goal.save()
        
        messages.success(request, f'Goal for {goal.month}/{goal.year} updated successfully.')
        return redirect('goal_list')
    
    # Generate year choices (current year and next 2 years)
    current_year = timezone.now().year
    year_choices = range(current_year - 1, current_year + 3)
    
    return render(request, 'goals/edit.html', {'goal': goal, 'year_choices': year_choices})


@login_required
def goal_delete(request, goal_id):
    goal = get_object_or_404(MonthlyGoal, id=goal_id, user=request.user)
    goal.save()
    goal.delete()
    messages.success(request, f'Goal for {goal.month}/{goal.year} deleted successfully.')
    return redirect('goal_list')


# API Views for Dashboard
@login_required
def api_payment_pipeline(request):
    """API endpoint for payment pipeline chart data"""
    months = int(request.GET.get('months', 6))
    
    pipeline_data = []
    for i in range(months):
        month_date = timezone.now().date().replace(day=1) - timezone.timedelta(days=30*i)
        month_payments = Payment.objects.filter(
            project__user=request.user,
            actual_date__year=month_date.year,
            actual_date__month=month_date.month,
            status='received'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        pipeline_data.append({
            'month': month_date.strftime('%b %Y'),
            'amount': float(month_payments)
        })
    
    pipeline_data.reverse()
    return JsonResponse({'data': pipeline_data})


@login_required
def api_project_stats(request):
    """API endpoint for project statistics"""
    total_projects = Project.objects.filter(user=request.user).count()
    active_projects = Project.objects.filter(user=request.user, status='in_progress').count()
    completed_projects = Project.objects.filter(user=request.user, status='completed').count()
    proposal_projects = Project.objects.filter(user=request.user, status='proposal').count()
    
    return JsonResponse({
        'total': total_projects,
        'active': active_projects,
        'completed': completed_projects,
        'proposal': proposal_projects
    })


@login_required
def profile_view(request):
    if request.method == 'POST':
        # Update user information
        user = request.user
        user.name = request.POST.get('name', user.name)
        user.email = request.POST.get('email', user.email)
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        # Handle password change
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if current_password and new_password and confirm_password:
            if user.check_password(current_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    messages.success(request, 'Password updated successfully.')
                else:
                    messages.error(request, 'New passwords do not match.', extra_tags='danger')
            else:
                messages.error(request, 'Current password is incorrect.', extra_tags='danger')
        
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    
    # Get user statistics
    total_projects = Project.objects.filter(user=request.user).count()
    total_payments = Payment.objects.filter(project__user=request.user).count()
    total_revenue = Payment.objects.filter(
        project__user=request.user, 
        status='received'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    active_projects = Project.objects.filter(
        user=request.user, 
        status='in_progress'
    ).count()
    
    context = {
        'total_projects': total_projects,
        'total_payments': total_payments,
        'total_revenue': total_revenue,
        'active_projects': active_projects,
    }
    
    return render(request, 'profile.html', context)


def terms_view(request):
    return render(request, 'terms.html')


def privacy_view(request):
    return render(request, 'privacy.html')



