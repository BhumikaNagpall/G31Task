from django.urls import path
from . import views

urlpatterns = [
    path('rewards/', views.reward_page, name='reward_page'),
    path('feedback/', views.feedback_page, name='feedback_page'),
]
