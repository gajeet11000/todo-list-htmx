from django.shortcuts import render, redirect
from datetime import date

from django.contrib import auth

from . models import List, Task
from . forms import CreateUserForm, LoginForm



def index(req):
    return render(req, "todo_app/index.html")

def register(req):
    if req.method == "GET":
        
        new_form = CreateUserForm()
        return render(req, "todo_app/register.html", {"form": new_form})
    
    elif req.method == "POST":
        
        filled_form = CreateUserForm(req.POST)
        if filled_form.is_valid():
            filled_form.save()
            return redirect("login")

def login(req):
    if req.method == "GET":
        
        new_form = LoginForm()
        return render(req, "todo_app/register.html", {"form": new_form})
    
    elif req.method == "POST":
        
        filled_form = LoginForm(req, req.POST)
        
        if filled_form.is_valid():
            username = req.POST.get("username")
            password = req.POST.get("password")
            
            user = auth.authenticate(req, username=username, password=password)
            
            if user is not None:
                auth.login(req, user)
                return redirect("dashboard")
    

def dashboard(req):
    return render(req, "todo_app/dashboard.html")