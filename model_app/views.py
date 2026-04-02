from django.shortcuts import render,redirect
from model_app.models import User,Message,MessageForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate


def posts(request):

    if request.method == "POST":
        form = MessageForm(request.POST)
        user = request.user
        if form.is_valid() and user.is_authenticated:
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
        return redirect("/posts")

    form = MessageForm()
    users = User.objects.all()
    msgs = Message.objects.select_related('user').all()
    data = {
        'users':  users,
        'msgs' : msgs,
        'form' : form,
    }
    return render(request,"posts.html",data)


def index(request):
    return render(request,"index.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request,"register.html",{"form":form})


def sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        user = authenticate(username=request.POST["username"],password=request.POST["password"])
        if user is not None:
            login(request, user)
            return redirect("/")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def exit(request):
    logout(request)
    return redirect("/")