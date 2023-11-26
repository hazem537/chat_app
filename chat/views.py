from django.shortcuts import render ,redirect
from .forms import SignUpForm
from django.contrib.auth import login


def index(request):
    return render(request ,"chat/index.html")


def signup(request):
    if request.method =="POST":
        form =  SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("index")
    else:
        form  =SignUpForm()
        return render(request,"chat/signup.html",{"form":form})    