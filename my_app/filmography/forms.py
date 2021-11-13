from django import forms
from django.contrib.auth.forms import UserCreationForm

class ActorForm(forms.Form):
    actor = forms.CharField(label="Name", max_length=100)

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
