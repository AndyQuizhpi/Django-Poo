from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm

# Create your views here.


def home(request):
    """Página de inicio pública."""
    return render(request, 'home.html')


def signup(request):
    """Registro de nuevos usuarios."""
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})

    if request.POST["password1"] != request.POST["password2"]:
        messages.error(request, "Las contraseñas no coinciden.")
        return render(request, 'signup.html', {
            "form": UserCreationForm,
            "error": "Passwords did not match."
        })

    try:
        user = User.objects.create_user(
            request.POST["username"], password=request.POST["password1"])
        user.save()
        login(request, user)
        messages.success(request, f"¡Bienvenido, {user.username}! Tu cuenta fue creada correctamente.")
        return redirect('tasks')
    except IntegrityError:
        messages.error(request, "Ese nombre de usuario ya existe.")
        return render(request, 'signup.html', {
            "form": UserCreationForm,
            "error": "Username already exists."
        })


def signin(request):
    """Inicio de sesión."""
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})

    user = authenticate(
        request, username=request.POST['username'], password=request.POST['password'])
    if user is None:
        messages.error(request, "Usuario o contraseña incorrectos.")
        return render(request, 'signin.html', {
            "form": AuthenticationForm,
            "error": "Username or password is incorrect."
        })

    login(request, user)
    messages.success(request, f"Sesión iniciada. ¡Hola, {user.username}!")
    return redirect('tasks')


@login_required
def signout(request):
    """Cierre de sesión."""
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect('home')


@login_required
def tasks(request):
    """Lista de tareas pendientes del usuario autenticado, con búsqueda y filtro."""
    task_list = Task.objects.filter(user=request.user, datecompleted__isnull=True)

    query = request.GET.get('q')
    if query:
        task_list = task_list.filter(
            Q(title__icontains=query) | Q(description__icontains=query))

    if request.GET.get('important') == '1':
        task_list = task_list.filter(important=True)

    task_list = task_list.order_by('-created')

    pending_count = Task.objects.filter(user=request.user, datecompleted__isnull=True).count()
    completed_count = Task.objects.filter(user=request.user, datecompleted__isnull=False).count()

    return render(request, 'tasks.html', {
        "tasks": task_list,
        "query": query or "",
        "important_only": request.GET.get('important') == '1',
        "pending_count": pending_count,
        "completed_count": completed_count,
    })


@login_required
def tasks_completed(request):
    """Historial de tareas completadas del usuario autenticado."""
    task_list = Task.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')

    pending_count = Task.objects.filter(user=request.user, datecompleted__isnull=True).count()
    completed_count = task_list.count()

    return render(request, 'completed_tasks.html', {
        "tasks": task_list,
        "pending_count": pending_count,
        "completed_count": completed_count,
    })


@login_required
def create_task(request):
    """Creación de una nueva tarea."""
    if request.method == "GET":
        return render(request, 'create_task.html', {"form": TaskForm()})

    form = TaskForm(request.POST)
    if form.is_valid():
        new_task = form.save(commit=False)
        new_task.user = request.user
        new_task.save()
        messages.success(request, "Tarea creada correctamente.")
        return redirect('tasks')

    messages.error(request, "No se pudo crear la tarea. Revisa los datos ingresados.")
    return render(request, 'create_task.html', {
        "form": form,
        "error": "Error creating task."
    })


@login_required
def task_detail(request, task_id):
    """Ver y actualizar el detalle de una tarea (solo si pertenece al usuario)."""
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})

    form = TaskForm(request.POST, instance=task)
    if form.is_valid():
        form.save()
        messages.success(request, "Tarea actualizada correctamente.")
        return redirect('tasks')

    messages.error(request, "No se pudo actualizar la tarea. Verifica los campos obligatorios.")
    return render(request, 'task_detail.html', {
        'task': task,
        'form': form,
        'error': 'Error updating task.'
    })


@login_required
def complete_task(request, task_id):
    """Marca una tarea como completada (solo vía POST y del propio usuario)."""
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        messages.success(request, f"«{task.title}» marcada como completada.")
        return redirect('tasks')
    return redirect('task_detail', task_id=task.id)


@login_required
def delete_task(request, task_id):
    """Elimina una tarea (solo vía POST y del propio usuario)."""
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f"«{title}» fue eliminada.")
        return redirect('tasks')
    return redirect('task_detail', task_id=task.id)
