from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone

def index(request):
    return render(request, 'index.html', {})

def signin(request):
    if request.method == 'GET':
        return render(request, 'task/signin.html', {'form':AuthenticationForm})
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request, 'task/signin.html', {'form':AuthenticationForm, 'error':'Usuario/Contraseña no es valido'})
        else:
            login(request, user)
            return redirect('task')

def signup(request):
    if request.method == 'GET':
        return render(request, 'task/index.html', {'form':UserCreationForm})
    else: 
        if request.POST['password1'] == request.POST['password2']:
                # registro de usuarios
            try:    
                user = User.objects.create_user(username = request.POST['username'], password= request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('task')
            except: # se puede agarrar el error IntegrityError para tomar el error en concreto a tratar (no lo hago v:)
                return render(request, 'task/index.html', {'form':UserCreationForm, 'error':'Usuario ya existe'})
        return render(request, 'task/index.html', {'form':UserCreationForm, 'error':'Contraseña no coincide'})

@login_required
def signout(request):
    logout(request)
    return redirect('index')



@login_required    
def task(request):
    try:
        tasks = Task.objects.filter(user = request.user)
        # tasks = Task.objects.all()
        return render(request, 'task/task.html', {'tasks':tasks})
    except TypeError:
        tasks = Task.objects.all()
        return render(request, 'task/task.html', {'tasks':tasks})
@login_required    
def task_detail(request, id_task):
    if request.method == 'GET':
        task = get_object_or_404(Task,pk = id_task)
        form = TaskForm(instance=task)
        contex = {
            'task':task,
            'form':form,
        }
        return render(request, 'task/task_detail.html', contex)
    else:
        task = get_object_or_404(Task,pk = id_task)
        form = TaskForm(request.POST, instance=task)
        form.save()
        return redirect('task')
@login_required    
def task_delete(request, id_task):
    task = get_object_or_404(Task, pk = id_task, user = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task')
@login_required    
def task_complete(request, id_task):
    task = get_object_or_404(Task, pk = id_task, user = request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('task')
@login_required    
def task_not_complete(request, id_task):
    task = get_object_or_404(Task, pk = id_task, user = request.user)
    if request.method == 'POST':
        task.datecompleted = None
        task.save()
        return redirect('task')  
@login_required    
def task_complete_all(request):
    try:
        tasks = Task.objects.filter(user = request.user)
        # tasks = Task.objects.all()
        return render(request, 'task/complete_all.html', {'tasks':tasks})
    except TypeError:
        tasks = Task.objects.all()
        return render(request, 'task/complete_all.html', {'tasks':tasks})
@login_required        
def create_task(request):
    if request.method == 'GET':
        return render(request, 'task/crud/create.html', {'form':TaskForm})
    if request.method == 'POST':
        form = TaskForm(request.POST)
        new_task = form.save(commit = False)
        new_task.user = request.user
        new_task.save()
        return redirect('task')