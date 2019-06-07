from django.db import models
from django.utils import timezone

# Create your models here.


class User(models.Model):
    name = models.TextField(max_length=200)
    email = models.EmailField(max_length=200)
    login = models.TextField(max_length=200)
    password = models.TextField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)


class Task(models.Model):
    LOW = 'L',
    MEDIUM = 'M',
    HIGH = 'H'
    PRIORITY_CHOICES = ((LOW, 'low'), (MEDIUM, 'medium'), (HIGH, 'high'))

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.TextField(max_length=254)
    prioprity = models.CharField(
        choices=PRIORITY_CHOICES, default=LOW, max_length=50)
    is_done = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    acomplish_date = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(days=1))
