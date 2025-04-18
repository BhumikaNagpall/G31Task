# from allauth.socialaccount.models import SocialAccount
# from django.shortcuts import redirect
# from django.urls import reverse
# from main.models import Profile
# from django.contrib.auth import get_user_model
# User=get_user_model()
# def social_user(strategy, details, user=None,uid=None, *args, **kwargs):
#     # if user:
#     #     try:
#     #         # Try to get the social account
#     #         social_account = SocialAccount.objects.get(user=user)
#     #         return social_account.user
#     #     except SocialAccount.DoesNotExist:
#     #         # Handle case where social account is missing
#     #         print("No social account linked to user.")
#     #         return None
#     # else:
#     #     print("No user provided.")
#     #     return None

#     if user:
#         try:
#             # Make sure 'uid' is passed correctly
#             if uid:
#                 social_account = SocialAccount.objects.get(user=user, uid=uid)
#                 return social_account.user
#             else:
#                 print("UID is missing!")
#                 return None
#         except SocialAccount.DoesNotExist:
#             # Handle case where social account is missing
#             print("No social account linked to user.")
#             return None
#     else:
#         print("No user provided.")
#         return None
# def update_user_profile(strategy, details, user=None, *args, **kwargs):
#     if user:
#         # Ensure name and phone are updated in case they are missing
#         if 'name' in details:
#             user.name = details['name']
#         if 'phone' in details:
#             user.phone = details['phone']
#         user.save()
        
#         # Profile.objects.get_or_create(user=user, phone=user.phone)
#         profile, created = Profile.objects.get_or_create(user=user)
#         profile.phone = user.phone
#         profile.save()

#         return user
#     else:
#         print("User object is None.")
#         return None
# from social_core.pipeline.social_auth import social_user

# def custom_social_user(backend, user, response, *args, **kwargs):
#     # Ensure 'uid' is present
#     uid = response.get('id')
#     if not uid:
#         raise ValueError("UID is missing in the response")
#     return social_user(backend, user, response, *args, **kwargs)
# auth_pipeline.py

def create_user_with_extra_fields(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'user': user}

    name = details.get('fullname') or details.get('first_name') or 'Anonymous'
    email = details.get('email')
    phone = ''  # or generate default or ask later

    return {
        'user': strategy.create_user(
            email=email,
            name=name,
            phone=phone,
        )
    }
