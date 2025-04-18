from django.shortcuts import render,redirect
from .models import Task
from main.models import AppUser
from django.contrib import messages
import calendar
from datetime import datetime
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404, redirect
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from .forms import UserEditForm
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
User=get_user_model()
from rewards.models import Reward


User = get_user_model()



@login_required
def calendar_view(request):
    tasks = Task.objects.filter(user=request.user, progress__lt=100)

    tasks_json = json.dumps([
        {
            'date': task.end_date.strftime('%Y-%m-%d'),
            'title': task.task_title
        } for task in tasks if task.end_date
    ], cls=DjangoJSONEncoder)

    return render(request, 'calendar.html', {
        'tasks_json': tasks_json
    })
def is_admin(user):
    return user.is_superuser or user.is_staff
# def delete_task_view(request, id):
#     # task = Task.objects.get(id=id,user=request.user)
#     # task.delete()
#     # Get the task by ID
#     task = Task.objects.get( id=id,user=request.user)

#     # Allow deletion only if the user is the task owner or admin
#     if task.user != request.user and not request.user.is_superuser:
#         return HttpResponseForbidden("You are not allowed to delete this task.")

#     # Delete the task
#     task.delete()

#     # Show a success message
#     messages.success(request, "Task deleted successfully.")

#     # Redirect to the task list or dashboard
#     return redirect('admin_tasks')
# 
@login_required
@user_passes_test(is_admin)
def delete_task_view_new(request, id):
    # Get the task by ID and ensure the task belongs to the logged-in user or is being accessed by an admin
    task = get_object_or_404(Task, id=id)

    # Check if the logged-in user is allowed to delete this task
    # if task.user != request.user and not is_admin(request.user):
    #     return HttpResponseForbidden("You are not allowed to delete this task.")

    # Delete the task
    task.delete()

    # Show a success message
    messages.success(request, "Task deleted successfully.")

    # Redirect to the task list or dashboard
    return redirect('admin_tasks')  
@login_required  # Redirect to login if not logged in
def dashboard_page(request):
    title_query = request.GET.get('title', '').strip()
    priority_query = request.GET.get('priority', '').strip()

    # Filter tasks for the current user only and not completed
    tasks = Task.objects.filter(user=request.user, progress__lt=100)

    # Apply search filters
    if title_query:
        tasks = tasks.filter(task_title__icontains=title_query)

    if priority_query:
        tasks = tasks.filter(task_priority__iexact=priority_query)

    # Task data for calendar
    tasks_json = json.dumps([
        {
            'date': task.end_date.strftime('%Y-%m-%d'),
            'title': task.task_title
        } for task in tasks if task.end_date
    ], cls=DjangoJSONEncoder)

    # Unique priorities for dropdown (filter by user's tasks only)
    all_priorities = Task.objects.filter(user=request.user).values_list('task_priority', flat=True).distinct()

    return render(request, 'dashboard.html', {
        'tasks': tasks,
        'tasks_json': tasks_json,
        'all_priorities': all_priorities,
    })
from django.contrib.auth import get_user_model
User=get_user_model()
# from django.db.models import Prefetch

def is_admin(user):
    return user.is_superuser 

@login_required
@user_passes_test(is_admin)
def admin_tasks_view(request):
    tasks = Task.objects.all().order_by('-start_date')
    users = User.objects.all()
    return render(request, 'admin_tasks.html', {'tasks': tasks, 'users':users})
# from django.db import IntegrityError
@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)

    # 🚫 Don't allow deleting staff or superuser
    if user_to_delete.is_staff or user_to_delete.is_superuser:
        messages.error(request, "Cannot delete staff or admin users.")
        return redirect('admin_tasks')

    try:
        # Delete user-related tasks
        Task.objects.filter(user=user_to_delete).delete()

        # Now delete the user
        user_to_delete.delete()
        messages.success(request, f'User {user_to_delete.name} deleted successfully.')

    except IntegrityError as e:
        messages.error(request, f"Error deleting user: {str(e)}")

    return redirect('admin_tasks') 


# Check if user is an admin (superuser)
def is_admin(user):
    return user.is_superuser  # Admin check

# Check if the user is a staff member
def is_staff(user):
    return user.is_staff  

@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(AppUser, id=user_id)  # Get AppUser instead of User
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.name} updated successfully!')
            return redirect('admin_tasks')  # Redirect back to admin tasks page
    else:
        form = UserEditForm(instance=user)

    return render(request, 'edit_user.html', {'form': form, 'user': user})

@login_required
@user_passes_test(is_staff)
def staff_tasks_view(request):
    tasks = Task.objects.all().order_by('-start_date')  # Fetch all tasks
    users = AppUser.objects.all()  # Fetch all AppUser instances (instead of User)
    return render(request, 'staff_tasks.html', {'tasks': tasks, 'users':users})
def add_task_view(request):
    
    if request.method == 'POST':
        id = request.POST.get('id')
        task_title = request.POST.get('task_title')
        task_description = request.POST.get('task_description')
        task_priority = request.POST.get('task_priority')
        # start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        if not (task_title and task_description and task_priority and end_date):
            messages.error(request,'All fields are required.') 
        elif Task.objects.filter(task_title=task_title).exists():
            messages.error(request,'A Task with such name already exists! Please enter a different one.....')
        else:
            Task.objects.create(
                task_title=task_title,
                task_description=task_description,
                task_priority=task_priority,
                end_date=end_date,
                user=request.user
            )
            messages.error(request,'Task added successfully!!')
            return redirect('dashboard_page')  # Ensure correct URL name in urls.py
    
    tasks = Task.objects.all()  # Fetch tasks to display after adding
    return render(request, 'addtask.html', {'tasks': tasks})

def delete_task_view(request, id):
    task = Task.objects.get(id=id,user=request.user)
    task.delete()
    return redirect('dashboard_page')

def edit_progress(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        progress = request.POST.get('progress')
        try:
            task.progress = int(progress)
            task.save()

            # 💡 Check if task is completed and user hasn't been rewarded yet
            if task.progress == 100 and not Reward.objects.filter(user=request.user, reason__icontains=task.task_title).exists():
                # Create a reward for the completed task
                Reward.objects.create(
                    user=request.user,
                    coins=30,
                    reason=f"🎯 Task '{task.task_title}' completed!"
                )

                # Redirect to the reward page after the task is completed
                return redirect('reward_page')  # Make sure this URL name is correct
            else:
                 return redirect('dashboard_page')  # Redirect to dashboard if not completed or already rewarded
        except ValueError:
            messages.error(request, "Invalid progress value. Please enter a valid number.")
    
    # If it's a GET request or any other request
    return render(request, 'edit_progress.html',{'task':task})

def completed_tasks(request):
    completed = Task.objects.filter(user=request.user,progress=100)
    task_data = [
        {
            'title': task.task_title,
            'description': task.task_description,
            'priority': task.task_priority,
            'start': task.start_date.strftime('%Y-%m-%d'),
            'end': task.end_date.strftime('%Y-%m-%d'),
        } for task in completed
    ]
    return render(request, 'completed_tasks.html', {
        'tasks': completed,
        'task_data': json.dumps(task_data),  # For JS
    })

def update_task_view(request, id):
    user = request.user    
    if user.is_superuser:
        task = get_object_or_404(Task, id=id)
    elif not user.is_staff:  # regular user
        task = get_object_or_404(Task, id=id, user=user)
    else:
        return HttpResponseForbidden("You are not allowed to update tasks.")

    if request.method == 'POST':
        task_title = request.POST.get('title')
        task_description = request.POST.get('description')
        end_date = request.POST.get('due_date')
        task_priority = request.POST.get('priority')

        if not task_title:
            messages.error(request, "Title is mandatory")
        elif Task.objects.filter(task_title=task_title).exclude(id=id).exists():
            messages.error(request, "Title with this name is already registered")
        else:
            task.task_title = task_title
            task.task_description = task_description
            task.end_date = end_date
            task.task_priority = task_priority
            task.save()
            messages.success(request, f"Task '{task}' updated successfully")
            return redirect('dashboard_page')  # Or your task list route

    return render(request, 'update_task.html', {'task': task})
def calender_view(request):
    tasks = Task.objects.filter(user=request.user,progress__lt=100)
    tasks_json = json.dumps([
        {
            'date': task.end_date.strftime('%Y-%m-%d'),
            'title': task.task_title
        } for task in tasks if task.end_date  # ensure end_date is not None
    ], cls=DjangoJSONEncoder)

    context = {
        'tasks': tasks,
        'tasks_json': tasks_json,
    }
    return render(request, 'calender.html', context)


def edit_task(request, id):
    task = get_object_or_404(Task, id=id)
   
    if request.method == 'POST':
        task_title = request.POST.get('title')
        task_description = request.POST.get('description')
        end_date = request.POST.get('due_date')
        task_priority = request.POST.get('priority')

        if not task_title:
            messages.error(request, "Title is mandatory")
        elif Task.objects.filter(task_title=task_title).exclude(id=id).exists():
            messages.error(request, "Title with this name is already registered")
        else:
            task.task_title = task_title
            task.task_description = task_description
            task.end_date = end_date
            task.task_priority = task_priority
            task.save()
            messages.success(request, f"Task '{task}' updated successfully")
            return redirect('admin_tasks')  # Or your task list route

    return render(request, 'edit_task.html', {'task': task})

@login_required
def task_list(request):
    if request.user.is_superuser or request.user.is_staff:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_user=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})
from django.contrib.auth.decorators import permission_required
