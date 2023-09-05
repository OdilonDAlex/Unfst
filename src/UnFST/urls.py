"""UnFST URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from UnFST.settings import MEDIA_URL, MEDIA_ROOT
from UnFST.views import homepage
from blog.views import blog_homepage, create_post, register, login, logout, remove_post, post_detail, love_or_not_post, \
    modify_post, post_comment, remove_comment
from fst.views import fst_homepage, create_cours

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name="homepage"),
    path('blog/', blog_homepage, name="blog_homepage"),
    path('fst/', fst_homepage, name="fst_homepage"),
    path('blog/create_post', create_post, name="createPost"),
    path('blog/register', register, name='register'),
    path('blog/login', login, name='login'),
    path('blog/logout', logout, name='logout'),
    path('blog/remove_post<int:post_id>', remove_post, name="remove_post"),
    path('blog/modify_post<int:post_id>', modify_post, name="modify_post"),
    path('blog/<str:post_slug>', post_detail, name="post_detail"),
    path('blog/love_post/', love_or_not_post, name="love_post"),
    path('blog/post_comment/', post_comment, name="post_comment"),
    path('blog/remove_comment/', remove_comment, name="remove_comment"),
    path('fst/create_cours/', create_cours, name="create_cours")
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
