from django import forms
from django.contrib.auth.models import User

from .models import Movies, Review


class MovieForm(forms.ModelForm):
    class Meta:
        model=Movies
        fields=['title','poster','desc','release','actors','actress','categories','trailer_link']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("comment", "rating")

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')