from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.utils import timezone
from datetime import date, datetime, timedelta

from .models import Task, Category, Tag
from .forms import TaskForm, SearchForm, CategoryForm


def index(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(author=request.user, is_completed=False)[:5]
        now = timezone.now()
        reminders = Task.objects.filter(
            author=request.user,
            reminder_date__lte=now.date(),
            is_completed=False
        )
    else:
        tasks = []
        reminders = []
    context = {'tasks': tasks, 'reminders': reminders}
    return render(request, 'index.html', context=context)


def about(request):
    return render(request, 'about.html')


@login_required
def tasks(request):
    tasks = Task.objects.filter(author=request.user)
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            from django.db.models import Q
            tasks = tasks.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tags__name__icontains=query) |
                Q(category__name__icontains=query)
            ).distinct()
    
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'active':
        tasks = tasks.filter(is_completed=False)
    elif filter_type == 'completed':
        tasks = tasks.filter(is_completed=True)
    elif filter_type == 'today':
        today = date.today()
        tasks = tasks.filter(due_date=today)
    elif filter_type == 'week':
        today = date.today()
        week_end = today + timedelta(days=7)
        tasks = tasks.filter(due_date__gte=today, due_date__lte=week_end)
    elif filter_type == 'overdue':
        today = date.today()
        tasks = [t for t in tasks.filter(is_completed=False) if t.is_overdue]
    
    category_id = request.GET.get('category')
    if category_id:
        tasks = tasks.filter(category_id=category_id)
    
    categories = Category.objects.all()
    context = {
        'tasks': tasks,
        'form': form,
        'filter_type': filter_type,
        'categories': categories,
        'selected_category': category_id
    }
    return render(request, 'tasks/list.html', context=context)


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)
    context = {'task': task}
    return render(request, 'tasks/detail.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            if not form.cleaned_data.get('due_time'):
                task.due_time = '00:00'
            task.save()
            form.save_m2m()
            new_tag_name = form.cleaned_data.get('new_tag', '').strip()
            if new_tag_name:
                new_tag, _ = Tag.objects.get_or_create(name=new_tag_name, author=request.user)
                task.tags.add(new_tag)
            return redirect('task-detail', task_id=task.id)
    else:
        form = TaskForm(user=request.user)
    categories = Category.objects.filter(author=request.user)
    context = {'form': form, 'categories': categories}
    return render(request, 'tasks/create.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)
    if task.is_completed:
        return redirect('task-detail', task_id=task.id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            new_tag_name = form.cleaned_data.get('new_tag', '').strip()
            if new_tag_name:
                new_tag, _ = Tag.objects.get_or_create(name=new_tag_name, author=request.user)
                task.tags.add(new_tag)
            return redirect('task-detail', task_id=task.id)
    else:
        form = TaskForm(instance=task, user=request.user)
    categories = Category.objects.filter(author=request.user)
    context = {'form': form, 'task': task, 'categories': categories}
    return render(request, 'tasks/edit.html', context)


@login_required
@require_http_methods(["POST"])
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)
    task.delete()
    return redirect('task-list')


@login_required
@require_http_methods(["POST"])
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)
    task.is_completed = not task.is_completed
    task.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'is_completed': task.is_completed})
    return redirect('task-list')


@login_required
def categories(request):
    cats = Category.objects.filter(author=request.user)
    for cat in cats:
        cat.task_count = cat.tasks.filter(author=request.user).count()
    context = {'categories': cats}
    return render(request, 'tasks/categories.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, user=request.user)
        if form.is_valid():
            category = form.save(commit=False)
            category.author = request.user
            category.save()
            return redirect('category-list')
    else:
        form = CategoryForm(user=request.user)
    context = {'form': form}
    return render(request, 'tasks/category_form.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def edit_category(request, cat_id):
    category = get_object_or_404(Category, id=cat_id, author=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm(instance=category, user=request.user)
    context = {'form': form, 'category': category}
    return render(request, 'tasks/category_form.html', context)


@login_required
@require_http_methods(["POST"])
def delete_category(request, cat_id):
    category = get_object_or_404(Category, id=cat_id, author=request.user)
    category.delete()
    return redirect('category-list')


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer, CategorySerializer


class TaskListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(author=self.request.user)
