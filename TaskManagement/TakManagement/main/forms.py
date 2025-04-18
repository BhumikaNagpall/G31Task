# accounts/forms.py
# from allauth.account.forms import SignupForm
# from django import forms
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class CompleteSignupForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['name', 'phone']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['name'].label = "Full Name"
#         self.fields['phone'].label = "Phone Number"


# class CustomSignupForm(SignupForm):
#     name = forms.CharField(max_length=100, label="Full Name")
#     phone = forms.CharField(max_length=15, label="Phone Number")

#     def save(self, request):
#         user = super().save(request)
#         user.name = self.cleaned_data['name']
#         user.phone = self.cleaned_data['phone']
#         user.save()

#         # Optionally create a profile (if not using signals)
#         from main.models import Profile
#         Profile.objects.get_or_create(user=user, phone=user.phone)

#         return user
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import AppUser  # Assuming this is your custom user model

# Define the UserEditForm directly in views.py
class UserEditForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ['name', 'phone', 'role', 'gender', 'address']  # Include fields that you want the user to edit

