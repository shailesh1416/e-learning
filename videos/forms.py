from django import forms
from django.contrib.auth.forms import UserCreationForm

class markVideoForm(forms.Form):
    videoId = forms.IntegerField(required=True)

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
