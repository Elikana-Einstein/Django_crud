from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils import timezone
from .models import Task
from django.db.models import Q
from friends.models import FriendRequest
from django.contrib.auth.decorators import login_required
from .forms import Taskform,EditTaskForm

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

@login_required
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

@login_required
def update_task(request,task_id):
    task=get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method == 'POST':
        form = EditTaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
        
    else:
        if task.due_date:
            due_date_str = task.due_date.strftime('%Y-%m-%d')
        else:
            due_date_str = ''
        form = EditTaskForm(instance=task, initial={'due_date': due_date_str})
        
    return render(request,'tasks/task_update.html',{'form':form,'task':task})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)  # Ensure user owns the task

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    #  Add an else block
    else:
         return render(request, 'tasks/task_delete.html', {'task': task})
   
@login_required
def complete_task(request, task_id):
    task=get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method == 'POST':
        task.completed = not task.completed
        task.save()
        return redirect('task_list')
    

@login_required
def get_friends_task(request):
    # Retrieve accepted friend requests where the logged-in user is involved
    friend_requests = FriendRequest.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user), status='accepted'
    )
    
    # Get the profiles of friends (excluding request.user)
    friend_users = [
        friend.sender if friend.receiver == request.user else friend.receiver
        for friend in friend_requests
    ]

    # Retrieve tasks assigned to these friends
    tasks = Task.objects.filter(user__in=friend_users)

    return render(request, 'tasks/friends_task.html', {'tasks': tasks})