from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ActorFormModel

class ActorForm(forms.Form):
    class Meta:
        model = ActorFormModel
        fields = ['user', 'date', 'fullname']


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
