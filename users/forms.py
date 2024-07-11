from django import forms
from .models import User


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]

    # def save(self, commit=True):
    #     return User.objects.create_user(self.cleaned_data["email"], self.cleaned_data["password"])
