from django.http import HttpResponse
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
        return render(req, "todo_app/login.html", {"form": new_form})
    
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
    if req.method == "GET":
        lists = List.objects.filter(user=req.user)
        
        context = {
            "list": None,
            "tasks": None
        }
        
        if lists.exists():
            recent_list = lists.order_by("-date").first()
            tasks = Task.objects.filter(list_id=recent_list)

            context['list'] = recent_list
            context['tasks'] = tasks
        else:
            new_list = List.objects.create(
                title=date.today().strftime("%d, %B"),
                user=req.user
            )
            context['list'] = new_list
            # context["tasks"] is already None
            
        return render(req, "todo_app/dashboard.html", context)
    
def save_task(req):
    if req.method == "POST":
        task = req.POST.get("new_task")
        list_id = req.POST.get("list_id")
        
        new_task = Task.objects.create(
            name=task,
            list_id=List.objects.get(id=list_id),
        )
        
        new_task.save()
        
        return HttpResponse("<li>" + task + "</li>")