from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder']="Enter username"
        self.fields['email'].widget.attrs['placeholder']="Enter email"
        self.fields['password1'].widget.attrs['placeholder']="Enter password"
        self.fields['password2'].widget.attrs['placeholder']="Confirm password"
