from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post

from .forms import NewPost


def index(request):
    posts = Post.objects.order_by('-date')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "NewPost": NewPost,
        "posts": Post.objects.order_by('-date'),
        'page_obj': page_obj
    })


def newPost(request):
    if request.method == "POST":
        form = NewPost(request.POST)

        if form.is_valid():
            content = form.cleaned_data["content"]
            user = request.user
            Post.objects.create(content=content, user=user, likes=0)

    return HttpResponseRedirect(reverse("index"))


def profile(request, username):
    try:
        user_profile = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User not found.")
    if request.user in user_profile.followers.all():
        isFollowing = True
    elif request.user not in user_profile.followers.all():
        isFollowing = False

    users_posts = Post.objects.filter(user=user_profile).order_by('-date')
    paginator = Paginator(users_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "user_profile": user_profile,
        'page_obj': page_obj,
        "isFollowing": isFollowing
    })

def follow(request, username):
    to_follow = User.objects.get(username=username)
    user = request.user
    to_follow.followers.add(user)
    return HttpResponseRedirect(reverse("profile", args=[username]))

def unfollow(request, username):
    to_unfollow = User.objects.get(username=username)
    user = request.user
    to_unfollow.followers.remove(user)
    return HttpResponseRedirect(reverse("profile", args=[username]))

def following(request):
    posts = Post.objects.order_by('-date')
    user = request.user
    following = []
    for post in posts:
        if post.user in user.following.all():
            following.append(post)

    paginator = Paginator(following, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "NewPost": NewPost,
        'page_obj': page_obj
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
