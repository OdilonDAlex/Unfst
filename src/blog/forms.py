from django import forms
from django.contrib import auth

from UnFST.settings import AUTH_USER_MODEL
from blog.models import Post, CustomUser


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'publication_date', 'slug', 'lovers')
        labels = {
            "title": "Titre",
            "content": "Contenu",
            "image": "image",
            "with_html": "Utiliser du html"
        }


class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'last_name', 'first_name', 'password')
        labels = {
            "username": "Nom d'utilisateur",
            "first_name": "Prénom",
            "last_name": "Nom",
            "password": "Mot de passe"
        }

        widgets = {
            "password": forms.PasswordInput(),
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data['username']
        password = cleaned_data['password']

        user = auth.authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError("Mot de passe ou courriel erronée!")

        return cleaned_data
