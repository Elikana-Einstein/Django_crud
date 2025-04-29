from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task
from django.contrib.auth.decorators import login_required
from .forms import Taskform

# Create your views here.

@login_required
def task_list(request):
    tasks=Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request,'registration/register.html',{'form':form})

def task_create(request):
    if request.method == 'POST':
        form = Taskform(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = Taskform()
    return render(request, 'tasks/task_create.html', {'form': form})
    