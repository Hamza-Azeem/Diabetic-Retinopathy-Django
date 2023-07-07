from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name='signup'),
    path("login/", auth_views.LoginView.as_view(template_name='retinoscope/login.html'), name='login'),
    path("logout/", views.logout, name='logout'),
    path("profile/<int:pk>/", views.profile, name="profile"),
    path("profile/change_password", views.change_password, name="change_password"),
    path("profile/edit-info", views.edit_profile_info, name="edit_info"),
    path("profile/<int:pk>/history", views.get_history, name="history"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='retinoscope/password_reset.html'),name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='retinoscope/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='retinoscope/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='retinoscope/password_reset_complete.html'),name='password_reset_complete'),
    path('verification/', include('verify_email.urls')),	
    path('profile/<int:pk>/classification', views.get_image, name='classify'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),


]

urlpatterns += staticfiles_urlpatterns()
