from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
# from django.contrib.auth.models import User
from .models import AppUser
from django.contrib.auth import get_user_model
User = get_user_model() 
from django.contrib.auth.decorators import login_required
from .models import Profile
from datetime import datetime, timedelta
from DashboardApp.models import Task
from django.contrib.auth import logout
from django.http import HttpResponseNotAllowed


# Create your views here.
def about_us(request):
    return render(request, 'about_us.html')

def base(request):
    return render(request, 'base.html')

def billing(request):
    return render(request, 'billing.html', {
        'banner_message': 'Manage your billing and subscription settings here.'
    })

def contact(request):
    return render(request, 'contact.html')

def features(request):
    return render(request, 'features.html', {
        'banner_message': 'Explore all our powerful features!'
    })

def feedback(request):
    return render(request, 'feedback.html')



def help(request):
    return render(request, 'help.html')

def inspiration_hub(request):
    return render(request, 'inspiration_hub.html')

def integrations(request):
    return render(request, 'integrations.html', {
        'banner_message': 'Connect with your favorite tools seamlessly.'
    })

def suggest(request):
    return render(request, 'suggest.html')

def teams(request):
    return render(request, 'teams.html', {
        'banner_message': 'Collaborate and manage your team efficiently.'
    })


def templates(request):
    return render(request, 'templates.html')

def troubleshoot(request):
    return render(request, 'troubleshooting.html', {
        'banner_message': 'Let’s fix any issues you’re facing.'
    })

def get_started(request):
    return render(request, 'get_started.html', {
        'banner_message': 'Welcome to the Get Started Page! Let’s begin your journey.'
    })

def continue_without(request):
    return render(request, 'continue_without_login.html')

# def index2(request):
#     return render(request, 'index2.html')

def index3(request):
    return render(request, 'index3.html')

def index(request):
    return render(request, 'index.html')

def base_exp(request):
    return render(request, 'base_exp')


def index2(request):
    sections = [
        {"title": "Get Started", "description": "Start using the platform quickly.", "route": "get_started"},
        {"title": "Features", "description": "Explore all features we offer.", "route": "features"},
        {"title": "Teams", "description": "Manage your team and roles.", "route": "teams"},
        {"title": "Billing", "description": "View and manage billing options.", "route": "billing"},
        {"title": "Troubleshooting", "description": "Fix common issues and errors.", "route": "troubleshoot"},
        {"title": "Integrations", "description": "Connect with other tools.", "route": "integrations"},
    ]
    return render(request, 'index2.html', {'sections': sections})


from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import AppUser  # Assuming you're using a custom user model (AppUser)
import re
def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        confirm_password = request.POST.get('confirm_password')

        address = request.POST.get('address')  # New field
        gender = request.POST.get('gender')  # New field

        role = request.POST.get('role')  # Get the role

        # Password mismatch check
        if not re.fullmatch(r'\d{10}', phone):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return render(request, 'sign_up_page.html')
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'sign_up_page.html')

        # Check if username or email already exists
        elif AppUser.objects.filter(name=name).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'sign_up_page.html')

        elif AppUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'sign_up_page.html')

        elif AppUser.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already registered.")
            return render(request, 'sign_up_page.html')
            # Create the user and set the role
        user = AppUser.objects.create_user(name=name, email=email, password=password, phone=phone, address=address, gender=gender)
        if role == 'admin':
            user.is_superuser= True  # Grant admin privileges
          # Staff can access admin features, but not superuser
        user.save()

            # Optional: Create a profile for the user
        profile = Profile(user=user)  # Assuming you have a profile model
        profile.save()

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('loginPage')

    return render(request, 'sign_up_page.html')



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
           
            
            if user.is_superuser:
                if not user.is_staff:
                    user.is_staff = True
                    user.save()
                # Redirect to the admin tasks page
                return redirect('admin_tasks')  # Make sure this URL exists in your urls.py
            else:
                # Redirect to the user's dashboard
                messages.success(request, 'Welcome back!')
                return redirect('dashboard_page') 
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'login_page.html')


def logout_view(request):
    if request.method == 'POST':  # Handle POST requests only
        logout(request)
        return redirect('index')  # Redirect to index page after logout
    return HttpResponseNotAllowed(['POST'])

@login_required
def home(request):
    return render(request, 'home.html')

from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404

def profile_view(request):
    user = request.user
    
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user)
        profile.save()

    
    # profile = get_object_or_404(Profile, user=user)

    all_tasks = Task.objects.filter(user=user)
    completed_tasks = all_tasks.filter(progress=100)
    in_progress_tasks = all_tasks.filter(progress__lt=100)

    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    tasks_this_week = all_tasks.filter(end_date__range=[start_of_week, end_of_week])
    completed_this_week = tasks_this_week.filter(progress=100)

    try:
        weekly_productivity = round((completed_this_week.count() / tasks_this_week.count()) * 100)
    except ZeroDivisionError:
        weekly_productivity = 0

    context = {
        'completed_tasks_count': completed_tasks.count(),
        'in_progress_count': in_progress_tasks.count(),
        'weekly_productivity': weekly_productivity,
        'profile': profile,
        'user_name': user.get_full_name() or user.name or user.email,
        'user_phone': profile.phone if profile.phone else "Not Provided",
    }
    
    return render(request, "profile.html", context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import UserEditForm
@login_required
def edit_profile(request, user_id):
    # Ensure the user can only edit their own profile
    if request.user.id != user_id:
        messages.error(request, "You can only edit your own profile.")
        return redirect('profile')  # Or any other redirect, like the dashboard

    user = get_object_or_404(AppUser, id=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Profile updated successfully!')
            return redirect('profile')  # Redirect to the profile page after saving changes
    else:
        form = UserEditForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form, 'user': user})


@login_required
def upload_profile_image(request):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        profile = request.user.profile
        profile.profile_image = request.FILES['profile_image']
        profile.save()
        
        
        return redirect('profile') 
    return redirect('profile')  # Adjust as necessary

@login_required
def delete_profile_image(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.profile_image.delete(save=True)
        return redirect('profile')

# def google_login_view(request):
#     return render(request,'login_page.html')

