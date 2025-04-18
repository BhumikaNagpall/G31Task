# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from DashboardApp.models import Task  # adjust to your real Task model
# from .models import Reward

# @receiver(post_save, sender=Task)
# def reward_user_on_completion(sender, instance, created, **kwargs):
#     if not created and instance.status == "Completed":  # Adjust status field
#         Reward.objects.get_or_create(
#             user=instance.user,  # adjust if different field
#             reason=f"Completed task: {instance.title}",
#             defaults={'coins': 10}
#         )
