from django import forms
from .models import Profile, FriendRequest, comment

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture','firstname','lastname','location','email','website']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'profile_picture': forms.ClearableFileInput(attrs={'multiple': False}),
        }

class friendRequestForm(forms.ModelForm):
    class Meta:
        model = FriendRequest
        fields = ['sender', 'receiver', 'status']