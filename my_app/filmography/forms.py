from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ActorUserRequest, UserProfile
from django.forms import ModelForm

class ActorUserRequestForm(ModelForm):
    class Meta:
        model = ActorUserRequest
        fields = ['phrase']

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
