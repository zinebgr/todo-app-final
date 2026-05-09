from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Task
from .forms import TaskForm
import json

def get_template(template_name, request):
    lang = request.session.get('language', 'ar')
    return f'{lang}/{template_name}'

def task_list(request):
    tasks = Task.objects.all()
    
    search_query = request.GET.get('search', '')
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    filter_status = request.GET.get('filter', 'all')
    if filter_status == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_status == 'pending':
        tasks = tasks.filter(completed=False)
    
    stats = {
        'total': Task.objects.count(),
        'completed': Task.objects.filter(completed=True).count(),
        'pending': Task.objects.filter(completed=False).count(),
    }
    
    context = {
        'tasks': tasks,
        'stats': stats,
        'search_query': search_query,
        'filter_status': filter_status,
    }
    return render(request, get_template('task_list.html', request), context)

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إنشاء المهمة بنجاح!' if request.session.get('language', 'ar') == 'ar' else 'Task created successfully!')
            return redirect('todo:task_list')
    else:
        form = TaskForm()
    
    context = {
        'form': form, 
        'title': 'إضافة مهمة جديدة' if request.session.get('language', 'ar') == 'ar' else 'Add New Task'
    }
    return render(request, get_template('task_form.html', request), context)

def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث المهمة بنجاح!' if request.session.get('language', 'ar') == 'ar' else 'Task updated successfully!')
            return redirect('todo:task_list')
    else:
        form = TaskForm(instance=task)
    
    context = {
        'form': form, 
        'title': 'تعديل المهمة' if request.session.get('language', 'ar') == 'ar' else 'Edit Task'
    }
    return render(request, get_template('task_form.html', request), context)

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'تم حذف المهمة بنجاح!' if request.session.get('language', 'ar') == 'ar' else 'Task deleted successfully!')
        return redirect('todo:task_list')
    
    context = {'task': task}
    return render(request, get_template('task_confirm_delete.html', request), context)

def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'completed': task.completed})
    
    return redirect('todo:task_list')

def update_task_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for order, task_id in enumerate(data['order']):
                Task.objects.filter(id=task_id).update(order=order)
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