from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('about/', views.about_us, name='about_us'),
    path('base/', views.base, name='base'),
    path('billing/', views.billing, name='billing'),
    path('contact/', views.contact, name='contact'),
    path('features/', views.features, name='features'),
    path('get_started/', views.get_started, name='get_started'),
    path('help/', views.help, name='help'),
    path('inspiration_hub/', views.inspiration_hub, name='inspiration_hub'),
    path('integrations/', views.integrations, name='integrations'),
    path('suggest/', views.suggest, name='suggest'),
    path('teams/', views.teams, name='teams'),
    path('templates/', views.templates, name='templates'),
    path('troubleshooting/', views.troubleshoot, name='troubleshoot'),
    path('continue/', views.continue_without, name='continue'),
    path('index2/', views.index2, name='index2'),
    path('index3/', views.index3, name='index3'),
    path('', views.index, name='index'),
    # path('login/', views.login_view, name='loginPage'),
    path("login/",views.login_view,name="loginPage"),
    path("signup/",views.signup_view,name="signup"),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html'), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('feedback/', views.feedback, name='feedback'),
    path('base_exp/', views.base_exp, name='base_exp'),
     path('home/', views.home, name='home'),
    path('profile/',views.profile_view, name='profile'),
    path('upload-profile-image/', views.upload_profile_image, name='upload_profile_image'),
    path('delete_profile_image/', views.delete_profile_image, name='delete_profile_image'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/<int:user_id>/', views.edit_profile, name='edit_profile'),

    # path('complete-signup/', views.complete_signup, name='complete_signup'),
]


