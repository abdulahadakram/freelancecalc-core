from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal


class User(AbstractUser):
    name = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    def get_initials(self):
        """Get user initials for profile display"""
        if self.name:
            names = self.name.split()
            if len(names) >= 2:
                return (names[0][0] + names[-1][0]).upper()
            elif len(names) == 1:
                return names[0][:2].upper()
        return self.username[:2].upper()
    
    def get_display_name(self):
        """Get display name for profile"""
        return self.name if self.name else self.username


class Client(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    class Meta:
        ordering = ['-created_at']


class Project(models.Model):
    PROJECT_TYPE_CHOICES = [
        ('hourly', 'Hourly'),
        ('fixed', 'Fixed Price'),
        ('retainer', 'Retainer'),
    ]
    
    PROJECT_STATUS_CHOICES = [
        ('proposal', 'Proposal'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='projects')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # Project details
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES, default='fixed')
    status = models.CharField(max_length=20, choices=PROJECT_STATUS_CHOICES, default='proposal')
    
    # Financial details
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    takeaway_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    costs = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Dates
    start_date = models.DateField()
    completion_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.client.name}"

    @property
    def net_profit(self):
        return self.takeaway_amount - self.costs

    class Meta:
        ordering = ['-created_at']


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('received', 'Received'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    expected_date = models.DateField()
    actual_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project.name} - {self.amount} - {self.status}"

    @property
    def is_overdue(self):
        if self.status == 'pending' and self.expected_date < timezone.now().date():
            return True
        return False

    class Meta:
        ordering = ['expected_date']


class MonthlyGoal(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='monthly_goals')
    year = models.IntegerField()
    month = models.IntegerField()
    income_goal = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.year}/{self.month:02d} - {self.income_goal}"

    class Meta:
        unique_together = ['user', 'year', 'month']
        ordering = ['-year', '-month']
