import datetime
from pathlib import Path

from django.db import models

from UnFST.settings import AUTH_USER_MODEL


class Parcours(models.Model):
    name = models.CharField(max_length=128, null=False)

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=128, null=False)

    def __str__(self):
        return self.name


class Cours(models.Model):
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    parcours = models.ManyToManyField(Parcours)
    niveau = models.ManyToManyField(Level)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="fst_file", blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

    def get_parcours(self):
        return ", ".join([parcours.name for parcours in self.parcours.all()])

    def get_levels(self):
        return ", ".join([niveau.name for niveau in self.niveau.all()])

    def get_file_size(self):
        if self.is_file_exist():
            return str(format(self.file.size / 1000000, '.2f'))
        return "file not found"

    def is_file_exist(self):
        try:
            self.file.size
        except:
            return False

        return True