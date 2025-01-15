# forms.py
from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'dark_mode', 'language', 'timezone', 'date_format', 'notifications_enabled',
            'email_verified', 'two_factor_auth', 'account_visibility', 'theme', 'font_size',
            'sidebar_position', 'share_activity', 'data_sharing', 'hide_profile_picture',
            'password_expiry_days', 'login_attempts_limit', 'allow_social_logins',
            'email_notifications', 'sms_notifications', 'push_notifications'
        ]
