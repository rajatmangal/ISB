
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import CreateUserForm, PostForm, CommentForm
from .decorators import unauthenticated_user


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

    context={'form': form}
    return render(request, 'posts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect.')
    context= {}
    return render(request, 'posts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    print(posts)
    return render(request, 'posts/dashboard.html', context)


@login_required(login_url='login')
def userPage(request):
    posts = Post.objects.all()
    context={'posts':posts}
    print(posts)
    return render(request, 'posts/dashboard.html', context)


@login_required(login_url='login')
def createPost(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.userid = request.user
            f.save();
            return redirect('home')
    context = {'form': form}
    return render(request, 'posts/newPost.html', context)


@login_required(login_url='login')
def viewPost(request, id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.userid = request.user
            f.postid = Post.objects.get(id = id)
            f.save()
    form = CommentForm();
    post = Post.objects.get(id=id)
    # url = 'createComment' + str(id)
    comments = PostComment.objects.filter(postid=post)
   # print(len(comments))
    context = { 'post': post, 'form':form, 'id':id, 'comments':comments};
    return render(request, 'posts/post.html',context)

