from datetime import date

from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#64748b')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories", null=True, blank=True)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['name', 'author'], name='unique_category_per_user')
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tags", null=True, blank=True)
    objects = models.Manager()

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['name', 'author'], name='unique_tag_per_user')
        ]

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Niski'),
        ('medium', 'Średni'),
        ('high', 'Wysoki'),
    ]

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="tasks")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    tags = models.ManyToManyField(Tag, blank=True, related_name="tasks")
    title = models.CharField(max_length=127, validators=[MinLengthValidator(3)])
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    due_time = models.TimeField(default='00:00')
    reminder_date = models.DateField(blank=True, null=True)
    reminder_time = models.TimeField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_completed = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        ordering = ['is_completed', 'due_date', 'due_time']

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        """Sprawdza czy zadanie jest po terminie (nieukończone i data/czas minął)"""
        from datetime import datetime
        if self.is_completed:
            return False
        now = datetime.now()
        task_deadline = datetime.combine(self.due_date, self.due_time)
        return now > task_deadline
