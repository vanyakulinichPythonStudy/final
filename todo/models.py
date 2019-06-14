from django.db import models
from django.utils import timezone
from django.utils.timezone import datetime
from django.contrib.auth.models import User


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Task(models.Model):
    LOW = 3
    MEDIUM = 2
    HIGH = 1
    PRIORITY_CHOICES = ((LOW, 'Low'), (MEDIUM, 'Medium'), (HIGH, 'High'))

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.TextField(max_length=254)
    priority = models.IntegerField(default=LOW, choices=PRIORITY_CHOICES)
    is_done = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    acomplish_date = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(days=1))

    def __str__(self):
        return self.name
