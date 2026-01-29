from django.core.exceptions import ValidationError
from django import forms
from django.core.validators import MinLengthValidator
from django.utils import timezone
from datetime import date

from .models import Task, Category, Tag


DEFAULT_TAGS = [
    'pilne', 'ważne', 'praca', 'dom', 'zakupy', 'studia', 'projekt',
    'zdrowie', 'rodzina', 'finanse', 'sport', 'hobby', 'spotkanie',
    'telefon', 'email', 'deadline', 'codzienne', 'tygodniowe'
]


def ensure_default_tags(user):
    """Tworzy domyślne tagi dla użytkownika jeśli nie istnieją"""
    if user:
        for tag_name in DEFAULT_TAGS:
            Tag.objects.get_or_create(name=tag_name, author=user)


class TaskForm(forms.ModelForm):
    new_tag = forms.CharField(
        required=False,
        max_length=30,
        label='Nowy tag',
        widget=forms.TextInput(attrs={
            'placeholder': 'Wpisz nazwę nowego tagu',
            'class': 'form-control'
        })
    )
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'required': 'required'}),
        error_messages={'required': 'Podaj datę wykonania zadania.'}
    )
    due_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time'}),
        initial='00:00'
    )
    reminder_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    reminder_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'tags', 'due_date', 'due_time', 'reminder_date', 'reminder_time', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Nazwa zadania',
                'required': 'required',
                'minlength': '3'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Opis zadania (opcjonalnie)'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '6'}),
            'priority': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
        }
        error_messages = {
            'title': {
                'required': 'Podaj nazwę zadania.',
                'min_length': 'Nazwa musi mieć minimum 3 znaki.',
            },
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user:
            ensure_default_tags(user)
            self.fields['category'].queryset = Category.objects.filter(author=user)
            self.fields['tags'].queryset = Tag.objects.filter(author=user)
        else:
            self.fields['category'].queryset = Category.objects.none()
            self.fields['tags'].queryset = Tag.objects.none()
        self.fields['category'].empty_label = "-- Wybierz kategorię --"
        self.fields['tags'].required = False
        if not self.instance.pk:
            self.fields['due_time'].initial = '00:00'

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError('Podaj nazwę zadania.')
        if len(title) < 3:
            raise ValidationError('Nazwa musi mieć minimum 3 znaki.')
        if self.user:
            existing = Task.objects.filter(title__iexact=title, author=self.user)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError('Zadanie o tej nazwie już istnieje.')
        return title

    def clean_new_tag(self):
        new_tag = self.cleaned_data.get('new_tag', '').strip()
        if new_tag and self.user:
            if Tag.objects.filter(name__iexact=new_tag, author=self.user).exists():
                raise ValidationError('Tag o tej nazwie już istnieje.')
        return new_tag

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if not due_date:
            raise ValidationError('Podaj datę wykonania zadania.')
        if due_date < date.today():
            raise ValidationError('Termin nie może być w przeszłości.')
        return due_date

    def clean(self):
        cleaned_data = super().clean()
        due_date = cleaned_data.get('due_date')
        reminder_date = cleaned_data.get('reminder_date')
        reminder_time = cleaned_data.get('reminder_time')
        
        if reminder_date and not reminder_time:
            raise ValidationError('Podaj godzinę przypomnienia.')
        if reminder_time and not reminder_date:
            raise ValidationError('Podaj datę przypomnienia.')
        if reminder_date and due_date:
            if reminder_date > due_date:
                raise ValidationError('Przypomnienie musi być przed terminem wykonania.')
        return cleaned_data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Nazwa kategorii',
                'required': 'required',
                'maxlength': '50'
            }),
            'color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'color-picker'
            }),
        }
        error_messages = {
            'name': {'required': 'Podaj nazwę kategorii.'},
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if self.user:
            existing = Category.objects.filter(name__iexact=name, author=self.user)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError('Kategoria o tej nazwie już istnieje.')
        return name

    def clean_color(self):
        color = self.cleaned_data.get('color')
        if self.user:
            existing = Category.objects.filter(color__iexact=color, author=self.user)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError('Ten kolor jest już używany przez inną kategorię.')
        return color


class SearchForm(forms.Form):
    query = forms.CharField(
        label='Szukaj',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Szukaj zadań...'})
    )
