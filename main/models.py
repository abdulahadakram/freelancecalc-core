from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=255, blank=True, null=True)
    survey_filled = models.BooleanField(default=False)


from django.db import models
from django.conf import settings


class UserOnboardingData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='onboarding_data')
    income_goal = models.CharField(max_length=255, blank=True, null=True)
    projects_per_month = models.CharField(max_length=255, blank=True, null=True)
    average_rate = models.CharField(max_length=255, blank=True, null=True)
    hours_per_week = models.CharField(max_length=255, blank=True, null=True)
    primary_industry = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_income_goal(self):
        return self.income_goal

    def get_projects_per_month(self):
        return self.projects_per_month

    def get_average_rate(self):
        return self.average_rate

    def get_hours_per_week(self):
        return self.hours_per_week

    def get_primary_industry(self):
        return self.primary_industry

    def __str__(self):
        return f'{self.user.username} - Onboarding Data'
