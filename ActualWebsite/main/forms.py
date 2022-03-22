from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Game, GameSegment
from .widgets import ClearableMultipleFilesInput
from .fields import MultipleFilesField
from django.forms import ModelForm
from accounts.models import Account
from django.core.validators import FileExtensionValidator
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Account
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm): # not really sure how this works, but oh well.
    username = UsernameField()


class ProfilePictureForm(forms.Form):

    user_picture = forms.ImageField(required=False)


class GameCreationForm(ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'summary', 'genre']


class GameSegmentCreationFormOne(ModelForm):
    class Meta:
        model = GameSegment

        fields = ['title', 'summary', 'genre']


class GameSegmentCreationFormTwo(forms.Form):

    thumbnail = forms.ImageField()
    html_file = forms.FileField(validators=[FileExtensionValidator(['html'])])
    # folder = MultipleFilesField(required=False, widget=ClearableMultipleFilesInput(attrs={'multiple': True})) to be used later




