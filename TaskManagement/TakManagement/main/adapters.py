from allauth.account.adapter import DefaultAccountAdapter
from .models import Profile

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit)
        
        # If you’re capturing phone or name in your signup form, you can access them here
        phone = form.cleaned_data.get('phone')
        name = form.cleaned_data.get('name')

        user.name = name
        user.phone = phone
        user.save()

        # Create user profile
        Profile.objects.get_or_create(user=user)

        return user
