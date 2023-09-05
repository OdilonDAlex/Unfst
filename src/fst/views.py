from django.http import HttpResponse
from django.shortcuts import render, redirect

from blog.views import get_logged_user
from fst.forms import CoursForm
from fst.models import Cours


# Create your views here.
def fst_homepage(request):
    all_cours = Cours.objects.all()

    cours_without_file_in_list = False
    for cours in all_cours:
        if not cours.is_file_exist():
            cours_without_file_in_list = True
            cours.delete()

    if cours_without_file_in_list:
        all_cours = Cours.objects.all()

    return render(request, "fst/fst.html", {"courss": all_cours})


def create_cours(request):
    logged_user = get_logged_user(request)

    if not logged_user:
        return redirect("login")

    form = CoursForm()
    if request.POST:

        form = CoursForm(request.POST, request.FILES)

        if form.is_valid():

            cours = form.save(commit=False)

            cours.save()

            if form.cleaned_data.get('niveau'):
                for niveau in form.cleaned_data['niveau']:
                    cours.niveau.add(niveau)

            if form.cleaned_data.get('parcours'):
                for parcours in form.cleaned_data['parcours']:
                    cours.parcours.add(parcours)

            cours.author = logged_user

            cours.save()

            return redirect("fst_homepage")

        return render(request, "fst/create_cours.html", {"form": form})

    return render(request, "fst/create_cours.html", {"form": form})
