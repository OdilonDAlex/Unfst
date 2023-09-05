from django import forms

from fst.models import Cours


class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        exclude = ('author', )
