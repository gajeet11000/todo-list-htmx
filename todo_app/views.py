from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import date

from django.contrib import auth

from . models import List, Task
from . forms import CreateUserForm, LoginForm

from django.core.exceptions import ValidationError

from django.db.models import Q

from django.contrib import messages

def index(req):
    return render(req, "todo_app/index.html")

def logout(req):
    auth.logout(req)
    messages.success(req, "Logged out successfully", extra_tags="logout")
    return redirect("index")

def register(req):
    if req.method == "GET":
        
        new_form = CreateUserForm()
        return render(req, "todo_app/register.html", {"form": new_form})
    
    elif req.method == "POST":
        
        filled_form = CreateUserForm(req.POST)
        if filled_form.is_valid():
            filled_form.save()
            
            messages.success(req, "User created successfully", extra_tags="register")
            
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
                
                messages.success(req, "Signed in successfully", extra_tags="login")
                
                return redirect("dashboard")
        else:
            return render(req, "todo_app/login.html", {"form": filled_form})
    

def dashboard(req):
    if req.method == "GET":
        return render(req, "todo_app/dashboard.html")
    
def save_task(req):
    if req.method == "POST":
        task = req.POST.get("new_task")
        list_id = req.POST.get("list_id")
        
        list = List.objects.get(id=list_id)
        
        new_task = Task.objects.create(
            name=task,
            list_id=list
        )
        
        new_task.save()
        all_tasks = Task.objects.filter(list_id=list_id)
        
        return render(req, "todo_app/partials/display_list.html", {"tasks": all_tasks, "list": list})
        
    
def update_task(req, task_id):
    task = Task.objects.get(id=task_id)
    if req.method == "GET":
        return render(req, "todo_app/partials/single_task.html", {"task": task})
    elif req.method == "PATCH":
        return render(req, "todo_app/partials/patch_task_container.html", {"task": task})
    elif req.method == "POST":
        new_task_name = req.POST.get("updated_task")
        task.name=new_task_name
        task.save()
        return render(req, "todo_app/partials/single_task.html", {"task": task})
    
def toggle_completion(req, task_id):
    if req.method == "PATCH":
        task = Task.objects.get(id=task_id)
        task.completed = not task.completed
        task.save()
        
        return JsonResponse({"success": True}, status=200)
    
def delete_task(req, task_id):
    if req.method == "DELETE":
        task = Task.objects.get(id=task_id)
        task.delete()
        
        return JsonResponse({"success": True}, status=200)
    
def create_new_list(req):
    if req.method == "POST":
        title = req.POST.get("list_title")
        try:
            new_list = List.objects.create(
                title=title,
                user=req.user
            )
            new_list.save()
            
            messages.success(req, new_list.title, extra_tags="create_list")
            
            return redirect('dashboard')
        except ValidationError:
            return JsonResponse({"success": False}, status=500)
        
def search_list(req):
    if req.method == "GET":
        search_input = req.GET.get("search_input", "")
        search_input = search_input.strip()
        
        context = {
            "search_results" : None
        }
        
        if search_input:
            words = search_input.split()
            query = Q(title__icontains=words[0])
            
            for word in words[1:]:
                query |= Q(title__icontains=word)
                
            lists_data = List.objects.filter(query, user=req.user).order_by("-date")
            
            context["search_results"] = lists_data
        else:
            context["search_results"] = List.objects.filter(user=req.user).order_by("-date")
        
        return render(req, "todo_app/partials/search_result.html", context)
    
def delete_list(req, list_id):
    if req.method == "DELETE":
        list = List.objects.get(id=list_id, user=req.user)
        list.delete()
         
        response =  JsonResponse({"success": True}, status=200)
        response["HX-Trigger"] = "customDeleteEvent"
        return response
    
def fetch_list(req):
    if req.method == "GET":
        list_id = req.GET.get("list_id", None)
        
        if list_id:
            context = {
                "list" : List.objects.get(user=req.user, id=list_id),
                "tasks" : Task.objects.filter(list_id=list_id),
            }
        else:
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
                
        return render(req, "todo_app/partials/display_list.html", context)
    
def update_list(req, list_id):
    list = List.objects.get(id=list_id)
    if req.method == "GET":
        return render(req, "todo_app/partials/list_title.html", {"list": list})
    elif req.method == "PATCH":
        return render(req, "todo_app/partials/patch_list_container.html", {"list": list})
    elif req.method == "POST":
        new_list_title = req.POST.get("updated_list")
        list.title=new_list_title
        list.save()
        return render(req, "todo_app/partials/list_title.html", {"list": list})