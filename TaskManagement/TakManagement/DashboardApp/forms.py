from django import forms
from django.contrib.auth import get_user_model
from .models import Task
User = get_user_model()

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'gender', 'role', 'address', 'is_active', 'is_staff']
        widgets = {
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
            'role': forms.TextInput(attrs={'placeholder': 'User Role'}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_title', 'task_description']  # only if all exist
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
