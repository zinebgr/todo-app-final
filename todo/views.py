from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Task
from .forms import TaskForm, CustomUserCreationForm
import json

def get_template(template_name, request):
    """إرجاع القالب المناسب حسب اللغة المختارة"""
    if request is None:
        return f'ar/{template_name}'
    lang = request.session.get('language', 'ar')
    return f'{lang}/{template_name}'

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'تم إنشاء الحساب بنجاح! مرحباً بك.' if request.session.get('language', 'ar') == 'ar' else 'Account created successfully! Welcome.')
            return redirect('todo:task_list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def task_list(request):
    tasks = request.user.tasks.all()
    
    search_query = request.GET.get('search', '')
    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    
    filter_status = request.GET.get('filter', 'all')
    if filter_status == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_status == 'pending':
        tasks = tasks.filter(completed=False)
    
    stats = {
        'total': tasks.count(),
        'completed': tasks.filter(completed=True).count(),
        'pending': tasks.filter(completed=False).count(),
    }
    
    context = {
        'tasks': tasks,
        'stats': stats,
        'search_query': search_query,
        'filter_status': filter_status,
    }
    return render(request, get_template('task_list.html', request), context)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'تم إنشاء المهمة بنجاح!' if request.session.get('language', 'ar') == 'ar' else 'Task created successfully!')
            return redirect('todo:task_list')
    else:
        form = TaskForm()
    
    context = {'form': form, 'title': 'إضافة مهمة جديدة' if request.session.get('language', 'ar') == 'ar' else 'Add New Task'}
    return render(request, get_template('task_form.html', request), context)

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث المهمة بنجاح!' if request.session.get('language', 'ar') == 'ar' else 'Task updated successfully!')
            return redirect('todo:task_list')
    else:
        form = TaskForm(instance=task)
    
    context = {'form': form, 'title': 'تعديل المهمة' if request.session.get('language', 'ar') == 'ar' else 'Edit Task'}
    return render(request, get_template('task_form.html', request), context)

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'تم حذف المهمة بنجاح!' if request.session.get('language', 'ar') == 'ar' else 'Task deleted successfully!')
        return redirect('todo:task_list')
    context = {'task': task}
    return render(request, get_template('task_confirm_delete.html', request), context)

@login_required
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'completed': task.completed})
    return redirect('todo:task_list')

@login_required
def update_task_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tasks = Task.objects.filter(user=request.user)
            for order, task_id in enumerate(data['order']):
                tasks.filter(id=task_id).update(order=order)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error'})

def change_language(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        if language in ['ar', 'en']:
            request.session['language'] = language
    return redirect(request.META.get('HTTP_REFERER', '/'))