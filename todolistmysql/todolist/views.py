from django.shortcuts import get_object_or_404, render, redirect
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView, CreateView, UpdateView)
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from todolist import forms
from django.db import connection
from todolist.forms import TaskForm, UserLoginForm, UpdateFormView
from django.utils.decorators import method_decorator
# Create your views here.

from django.utils import timezone
import pytz

class IndexView(TemplateView):
    template_name = 'index.html'
    
class SingUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('todolist:login')
    template_name = 'signup.html'
    
class LoginView(LoginView):
    authentication_form = forms.UserLoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('todolist:index') 
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            
            user_id = request.user.id
            title = form.cleaned_data['title']
            completed = form.cleaned_data['completed']
            utc_time = timezone.now()
            poland_timezone = pytz.timezone('Europe/Warsaw')
            local_time_poland = utc_time.astimezone(poland_timezone)
            
            # task = form.save(commit=False)
            # task.user = request.user
            # task.save()
            
            with connection.cursor() as cursor:
                user_id = request.user.id
                cursor.execute("SELECT * FROM todolist_task WHERE user_id = %s", [user_id])
                cursor.execute("INSERT INTO todolist_task(title, completed, created_at, user_id) VALUES (%s, %s, %s, %s)", [title,completed,local_time_poland,user_id])
                tasks = cursor.fetchall()
            
            print(user_id)
            print(title)
            print(completed)
            print(local_time_poland)
            print(tasks)
            
            return redirect('todolist:task_list')
    else:
        form = TaskForm()
    return render(request, 'add.html', {'form': form})

def task_list(request):
    # tasks = Task.objects.filter(user=request.user)  # Pobierz zadania dla zalogowanego użytkownika
     
    with connection.cursor() as cursor:
        user_id = request.user.id
        cursor.execute("SELECT * FROM todolist_task WHERE user_id = %s", [user_id])
        tasks = cursor.fetchall()
    
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def task_completed(request,task_id):
    with connection.cursor() as cursor:
          cursor.execute("UPDATE todolist_task SET completed='1' WHERE id=%s" ,[task_id])
          
    with connection.cursor() as cursor:
        user_id = request.user.id
        cursor.execute("SELECT * FROM todolist_task WHERE user_id = %s", [user_id])
        tasks = cursor.fetchall()
    return render(request, 'task_list.html',{'tasks': tasks})

@login_required
def delete_task(request,task_id):
    with connection.cursor() as cursor:
          cursor.execute("DELETE FROM todolist_task WHERE id=%s" ,[task_id])
    
    with connection.cursor() as cursor:
        user_id = request.user.id
        cursor.execute("SELECT * FROM todolist_task WHERE user_id = %s", [user_id])
        tasks = cursor.fetchall()
    return render(request, 'task_list.html',{'tasks': tasks})

@method_decorator(login_required, name='dispatch')
class TaskEditView(UpdateView):
    model = Task
    template_name = 'edit_task.html'  # Template for editing
    success_url = '/task_list/'  # URL to redirect after successful update
    form_class = UpdateFormView
    
    def get_object(self, queryset=None):
        pk = self.kwargs.get('task_id')  # Retrieve the pk from URL parameters
        return Task.objects.get(pk=pk)