from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('tasks/', views.tasks, name='task-list'),
    path('tasks/<int:task_id>/', views.task_detail, name='task-detail'),
    path('tasks/create/', views.create_task, name='task-create'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='task-edit'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='task-delete'),
    path('tasks/<int:task_id>/toggle/', views.toggle_task, name='task-toggle'),
    path('categories/', views.categories, name='category-list'),
    path('categories/create/', views.create_category, name='category-create'),
    path('categories/<int:cat_id>/edit/', views.edit_category, name='category-edit'),
    path('categories/<int:cat_id>/delete/', views.delete_category, name='category-delete'),
    path('api/tasks/', views.TaskListAPIView.as_view(), name='api-tasks'),
    path('api/categories/', views.CategoryListAPIView.as_view(), name='api-categories'),
]
