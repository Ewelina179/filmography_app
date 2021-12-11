from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import ActorUserRequest
from django.forms import ModelForm

class ActorUserRequestForm(ModelForm):
    class Meta:
        model = ActorUserRequest
        fields = ['phrase']

    def clean(self):
        #print(self.user)
        if self.user.userprofile.daily_api_counter > 10:
            raise ValidationError('Przekroczono dozwoloną liczbę zapytań do API')
        pass

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
