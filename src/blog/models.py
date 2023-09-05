import datetime
import time

from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

from UnFST.settings import AUTH_USER_MODEL


class CustomUser(AbstractUser):
    interaction_number = models.IntegerField(default=0)
    love_count = models.IntegerField(default=0)
    post_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)


class Post(models.Model):
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField()
    publication_date = models.DateTimeField()
    image = models.ImageField(upload_to="blog_image", blank=True, null=True)
    with_html = models.BooleanField(default=False)
    lovers = models.ManyToManyField(AUTH_USER_MODEL, related_name="post_lovers")

    def clean(self):
        cleaned_data = super().clean()

        self.slug = slugify(self.title + str(time.time()).split(".")[0])

        self.publication_date = datetime.datetime.now()

        return cleaned_data

    def __str__(self):
        return f"{self.title}"

    def get_content_number_of_words(self):
        return len(self.content.split())

    def get_love_number(self):
        if self.lovers.all():
            return len(self.lovers.all())

        return 0

    def get_comments(self):
        if self.postcomment_set.all():
            comments = list(self.postcomment_set.all().order_by("-comment_date"))

            if len(comments) > 5:
                return comments[:5]
            return comments

    def comment_number(self):
        if self.postcomment_set.all():
            return len(self.postcomment_set.all())

        return 0

    @property
    def get_interaction_number(self):
        return sum([self.get_love_number(), self.comment_number()])

    def content_len_words(self):
        return len(self.content.split())


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    content = models.TextField(null=False)
    comment_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Commentaire({self.author.get_full_name()}, {self.content})"
