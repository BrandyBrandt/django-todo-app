from django.contrib import admin
from .models import Task, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'due_date', 'due_time', 'priority', 'is_completed')
    list_filter = ('priority', 'is_completed', 'category', 'due_date')
    search_fields = ('title', 'description')
    ordering = ('is_completed', 'due_date')
