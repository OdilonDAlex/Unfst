import datetime
from pprint import pprint

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from blog.forms import PostForm, RegisterForm, LoginForm
from blog.models import Post, CustomUser, PostComment

User = auth.get_user_model()


def blog_homepage(request):
    all_user_post = Post.objects.all().order_by("-publication_date")
    top_contributor = CustomUser.objects.all().order_by("interaction_number")

    all_user_post_copy = list(all_user_post).copy()
    all_user_post_copy.sort(key=lambda post: post.get_interaction_number, reverse=True)

    top_posts = all_user_post_copy[:10]

    top_contributor = list(top_contributor)[:50]

    for index in range(-len(top_contributor), 0):
        if top_contributor[index].interaction_number > 0:
            break

        print(top_contributor[index], top_contributor[index].interaction_number)
        top_contributor.pop(index)

    top_contributor.reverse()
    if len(all_user_post) > 10:
        all_user_post = all_user_post[:10]

    return render(request, "blog/blog.html",
                  {"posts": all_user_post, "contributors": top_contributor, "top_posts": top_posts})


def create_post(request):
    form = PostForm()
    user = get_logged_user(request)

    if not user:
        return redirect('login')

    if request.POST:
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.save()
            user.interaction_number += 1
            user.post_count += 1
            user.save()
            return redirect('blog_homepage')

    emoji_left_list = [number for number in range(128512, 128578)]
    emoji_right_list = [number for number in range(129296, 129332)]
    emoji_right_list.extend([number for number in range(128064, 128082)])
    emoji_right_list.extend([number for number in range(128123, 128135)])

    return render(request, "blog/create_post.html", {"form": form, "buttonName": "Publier",
                                                     "emoji_left_list": emoji_left_list,
                                                     "emoji_right_list": emoji_right_list})


def register(request):
    form = RegisterForm()

    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data.get('username'),
                                            password=data.get('password'),
                                            first_name=data.get('first_name'),
                                            last_name=data.get('last_name'))

            auth.login(request, user=user)
            request.session['user_id'] = user.id
            return redirect('blog_homepage')

        else:
            return render(request, 'blog/register.html', {"form": form})

    return render(request, 'blog/register.html', {"form": form})


def get_logged_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = CustomUser.objects.get(id=user_id)
        except:
            return None

        return user
    return None


def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            request.session['user_id'] = user.id
            return redirect('blog_homepage')

        return render(request, 'blog/login.html', {"login_error": True})

    return render(request, 'blog/login.html', {"login_error": False})


def logout(request):
    auth.logout(request)
    return redirect('blog_homepage')


def modify_post(request, post_id):
    emoji_left_list = [number for number in range(128512, 128578)]
    emoji_right_list = [number for number in range(129296, 129332)]
    emoji_right_list.extend([number for number in range(128064, 128082)])
    emoji_right_list.extend([number for number in range(128123, 128135)])
    if request.POST:
        post = Post.objects.get(id=post_id)
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect("blog_homepage")
        else:
            return render(request, "blog/create_post.html",
                          {"form": form, "buttonName": "Modifier", "post_id": post_id,
                           "emoji_left_list": emoji_left_list,
                           "emoji_right_list": emoji_right_list})

    if post_id:
        try:
            post = Post.objects.get(id=post_id)
        except:
            return redirect('blog_homepage')

        return render(request, "blog/create_post.html", {"form": PostForm(instance=post), "buttonName": "Modifier",
                                                         "emoji_left_list": emoji_left_list,
                                                         "emoji_right_list": emoji_right_list
                                                         })

    return redirect('blog_homepage')


def remove_post(request, post_id):
    if post_id:
        try:
            post = Post.objects.get(id=post_id)

        except:
            return redirect('homepage')

        if post.author.post_count > 0:
            post.author.post_count -= 1
        post.author.save()
        post.delete()
        return redirect('blog_homepage')
    return redirect('homepage')


def post_detail(request, post_slug):
    if post_slug:
        try:
            post = Post.objects.get(slug=post_slug)
        except:
            return redirect('blog_homepage')

        return render(request, "blog/blog_detail.html", {"post": post})

    return redirect('blog_homepage')


def love_or_not_post(request):
    logged_user = get_logged_user(request)
    if 'post_id' in request.GET:

        if not logged_user:
            print("not logged")
            return HttpResponse("")

        try:
            post = Post.objects.get(id=request.GET['post_id'])
        except:
            return HttpResponse("")

        print(logged_user, post)
        if logged_user in post.lovers.all():

            if logged_user.love_count > 0:
                logged_user.love_count -= 1
            post.lovers.remove(logged_user)

        else:
            logged_user.interaction_number += 1
            logged_user.love_count += 1
            post.lovers.add(logged_user)

        logged_user.save()
        post.save()

    return HttpResponse(str(len(post.lovers.all())))


def post_comment(request):
    logged_user = get_logged_user(request)

    if not logged_user:
        return redirect('blog_homepage')

    try:
        comment_content = request.GET['comment_content']
        post_id = request.GET['post_id']

        post = Post.objects.get(id=post_id)

    except:
        print("Exception")
        return redirect('blog_homepage')

    comment = PostComment(post=post, author=logged_user, content=comment_content, comment_date=datetime.date.today())
    comment.save()
    logged_user.interaction_number += 1
    logged_user.comment_count += 1
    logged_user.save()
    return HttpResponse(logged_user.get_full_name() + f",{comment.id}")


def remove_comment(request):
    if request.GET:
        try:
            comment = PostComment.objects.get(id=request.GET['comment_id'])
        except:
            return ""

        if comment.author.comment_count > 0:
            comment.author.comment_count -= 1

        comment.delete()
        comment.author.save()
        return HttpResponse("OK")
    return redirect('blog_homepage')
