from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_main.forms import TaskForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Task, Taskpriority, Taskstatus

class TaskList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Task
    template_name = 'dfirtrack_main/task/task_list.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " TASK_LIST_ENTERED")
        return Task.objects.filter(Q(taskstatus_id=1) | Q(taskstatus_id=2))

class TaskClosed(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Task
    template_name = 'dfirtrack_main/task/task_closed.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " TASK_CLOSED_ENTERED")
        return Task.objects.filter(taskstatus_id=3)

class TaskAll(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Task
    template_name = 'dfirtrack_main/task/task_all.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " TASK_ALL_ENTERED")
        return Task.objects.all()

class TaskDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Task
    template_name = 'dfirtrack_main/task/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object
        task.logger(str(self.request.user), " TASK_DETAIL_ENTERED")
        return context

class TaskCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Task
    form_class = TaskForm
    template_name = 'dfirtrack_main/task/task_add.html'

    def get(self, request, *args, **kwargs):

        # get id of first status objects sorted by name
        taskpriority = Taskpriority.objects.order_by('taskpriority_name')[0].taskpriority_id
        taskstatus = Taskstatus.objects.order_by('taskstatus_name')[0].taskstatus_id

        if 'system' in request.GET:
            system = request.GET['system']
            form = self.form_class(initial={
                'system': system,
                'taskpriority': taskpriority,
                'taskstatus': taskstatus,
            })
        else:
            form = self.form_class(initial={
                'taskpriority': taskpriority,
                'taskstatus': taskstatus,
            })
        debug_logger(str(request.user), " TASK_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.task_created_by_user_id = request.user
            task.task_modified_by_user_id = request.user
            # adapt starting and finishing time corresponding to taskstatus
            if task.taskstatus == Taskstatus.objects.get(taskstatus_name="20_working"):
                task.task_started_time = timezone.now()
            elif task.taskstatus == Taskstatus.objects.get(taskstatus_name="30_done"):
                task.task_started_time = timezone.now()
                task.task_finished_time = timezone.now()
            task.save()
            form.save_m2m()
            task.logger(str(request.user), " TASK_ADD_EXECUTED")
            messages.success(request, 'Task added')
            # conditional redirect
            if 'system' in request.GET:
                system = request.GET['system']
                return redirect(reverse('system_detail', args=(system,)))
            else:
                return redirect(reverse('task_detail', args=(task.task_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class TaskUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Task
    form_class = TaskForm
    template_name = 'dfirtrack_main/task/task_edit.html'

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        form = self.form_class(instance=task)
        task.logger(str(request.user), " TASK_EDIT_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        form = self.form_class(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.task_modified_by_user_id = request.user
            # adapt starting and finishing time corresponding to taskstatus
            if task.taskstatus == Taskstatus.objects.get(taskstatus_name="10_pending"):
                task.task_started_time = None
                task.task_finished_time = None
            elif task.taskstatus == Taskstatus.objects.get(taskstatus_name="20_working"):
                task.task_started_time = timezone.now()
                task.task_finished_time = None
            elif task.taskstatus == Taskstatus.objects.get(taskstatus_name="30_done"):
                task.task_finished_time = timezone.now()
                if task.task_started_time == None:
                    task.task_started_time = timezone.now()
            task.save()
            form.save_m2m()
            task.logger(str(request.user), " TASK_EDIT_EXECUTED")
            messages.success(request, 'Task edited')
            # conditional redirect
            if 'system' in request.GET:
                system = request.GET['system']
                return redirect(reverse('system_detail', args=(system,)))
            else:
                return redirect(reverse('task_detail', args=(task.task_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class TaskStart(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Task

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        task.task_started_time = timezone.now()
        task.taskstatus = Taskstatus.objects.get(taskstatus_name="20_working")
        task.save()
        task.logger(str(request.user), " TASK_START_EXECUTED")
        messages.success(request, 'Task started')
        if 'system' in request.GET:
            system = request.GET['system']
            return redirect(reverse('system_detail', args=(system,)))
        else:
            return redirect(reverse('task_detail', args=(task.task_id,)))

class TaskFinish(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Task

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        self.setDone(task, request)
        messages.success(request, 'Task finished')
        if 'system' in request.GET:
            system = request.GET['system']
            return redirect(reverse('system_detail', args=(system,)))
        else:
            return redirect(reverse('task_detail', args=(task.task_id,)))

    @staticmethod
    def setDone(task, request):
        # set starting time if task was not started yet
        if task.task_started_time == None:
            task.task_started_time = timezone.now()
        task.task_finished_time = timezone.now()
        task.taskstatus = Taskstatus.objects.get(taskstatus_name="30_done")
        task.save()
        task.logger(str(request.user), " TASK_FINISH_EXECUTED")

class TaskRenew(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Task

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        task.task_started_time = None
        task.task_finished_time = None
        task.taskstatus = Taskstatus.objects.get(taskstatus_name="10_pending")
        task.task_assigned_to_user_id = None
        task.save()
        task.logger(str(request.user), " TASK_RENEW_EXECUTED")
        messages.warning(request, 'Task renewed')
        if 'system' in request.GET:
            system = request.GET['system']
            return redirect(reverse('system_detail', args=(system,)))
        else:
            return redirect(reverse('task_detail', args=(task.task_id,)))

class TaskSetUser(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Task

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        task.task_assigned_to_user_id = request.user
        task.save()
        task.logger(str(request.user), " TASK_SET_USER_EXECUTED")
        messages.success(request, 'Task assigned to you')
        if 'system' in request.GET:
            system = request.GET['system']
            return redirect(reverse('system_detail', args=(system,)))
        else:
            return redirect(reverse('task_detail', args=(task.task_id,)))

class TaskUnsetUser(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Task

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        task.task_assigned_to_user_id = None
        task.save()
        task.logger(str(request.user), " TASK_UNSET_USER_EXECUTED")
        messages.warning(request, 'User assignment for task deleted')
        if 'system' in request.GET:
            system = request.GET['system']
            return redirect(reverse('system_detail', args=(system,)))
        else:
            return redirect(reverse('task_detail', args=(task.task_id,)))
