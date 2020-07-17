import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


from .models import User, Post

from .forms import NewPost

def index(request):
    # retrieve posts
    posts = Post.objects.order_by('-date')

    # paginator
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
            Post.objects.create(content=content, user=user)

    return HttpResponseRedirect(reverse("index"))


def profile(request, username):
    # make sure user exists
    try:
        user_profile = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User not found.")

    # check if current user is following
    if request.user in user_profile.followers.all():
        isFollowing = True
    elif request.user not in user_profile.followers.all():
        isFollowing = False

    # get posts to display
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

@login_required
def following(request):
    # get posts
    posts = Post.objects.order_by('-date')
    user = request.user
    following = []

    # make a list of posts from following users
    for post in posts:
        if post.user in user.following.all():
            following.append(post)

    # display following posts
    paginator = Paginator(following, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "NewPost": NewPost,
        'page_obj': page_obj
    })

@login_required
@csrf_exempt
def postAPI(request, postId):
    # Query for requested post
    try:
        post = Post.objects.get(pk=postId)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data.get("content")
            post.save()
        elif data.get("likes") is not None:
            if data.get("like"):
                post.likes.add(request.user)
            else:
                post.likes.remove(request.user)
            post.save()
        return HttpResponse(status=204)

    elif request.method == "GET":
        return JsonResponse(post.serialize())

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

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
