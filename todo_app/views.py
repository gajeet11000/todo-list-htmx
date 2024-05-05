from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import date

from django.contrib import auth

from . models import List, Task
from . forms import CreateUserForm, LoginForm

from django.core.exceptions import ValidationError

from django.db.models import Q

from django.contrib import messages

from .custom_scripts.template_paths import *



def index(req):
    if req.user.is_authenticated:
        return redirect("dashboard")
    else:
        return render(req, templates["index"])







def dashboard(req):
    if req.method == "GET":
        return render(req, templates["dashboard"])
    
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
        
        return render(req, dashboard_contents["todo_list"], {"tasks": all_tasks, "list": list, "filter_toggled": "all"})
        
    
def update_task(req, task_id):
    task = Task.objects.get(id=task_id)
    if req.method == "GET":
        return render(req, dashboard_contents["single_task"], {"task": task})
    elif req.method == "PATCH":
        return render(req, patch_contents["task"], {"task": task})
    elif req.method == "POST":
        new_task_name = req.POST.get("updated_task")
        task.name=new_task_name
        task.save()
        return render(req, dashboard_contents["single_task"], {"task": task})
    
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
        
        return render(req, dashboard_contents["search_result"], context)
    
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
        filter = req.GET.get("filter", None)
        
        if list_id:
            list = List.objects.get(user=req.user, id=list_id)
            
            if filter == "pending":
                tasks = Task.objects.filter(list_id=list, completed=False)
            elif filter == "completed":
                tasks = Task.objects.filter(list_id=list, completed=True)
            else:
                tasks = Task.objects.filter(list_id=list)
                filter = "all"
                
            context = {
                "list" : list,
                "tasks": tasks,
                "filter_toggled": filter
            }
        else:
            lists = List.objects.filter(user=req.user)
            
            context = {
                "list": None,
                "tasks": None,
                "filter_toggled": "all"
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
        return render(req, dashboard_contents["todo_list"], context)
    
def update_list(req, list_id):
    list = List.objects.get(id=list_id)
    if req.method == "GET":
        return render(req, dashboard_contents["list_title"], {"list": list})
    elif req.method == "PATCH":
        return render(req, patch_contents["list"], {"list": list})
    elif req.method == "POST":
        new_list_title = req.POST.get("updated_list")
        list.title=new_list_title
        list.save()
        return render(req, dashboard_contents["list_title"], {"list": list})