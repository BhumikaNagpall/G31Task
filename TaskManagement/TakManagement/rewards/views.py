from django.shortcuts import render, redirect
from .models import Reward, Feedback
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def reward_page(request):
    user_rewards = Reward.objects.filter(user=request.user).order_by('-date_awarded')
    return render(request, 'reward_page.html', {'rewards': user_rewards})

@login_required
def feedback_page(request):
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comments = request.POST.get('comments')
        task_title = request.POST.get('task_title')

        Feedback.objects.create(
            user=request.user,
            rating=rating,
            comments=comments,
            task_title=task_title
        )
        messages.success(request, "Thanks for your feedback!")
        return redirect('reward_page')

    return render(request, 'feedback_form.html')

