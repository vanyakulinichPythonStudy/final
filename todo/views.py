from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
import datetime
from .models import Project, Task
from .forms import SignInForm, SignUpForm
from .utils.user_utils import authenticateUser
from .utils.tasks_utils import flattenTasks


def signin(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            user = authenticateUser(form)
            if user is not None:
                login(request, user)
                return redirect('/dashboard/')
            else:
                form.add_error('password', 'Invalid password. Try again')
        return render(request, 'signin.html', {'form': form})

    return render(request, 'signin.html', {'form': SignInForm()})


def signout(request):
    logout(request)
    return redirect('/signin/')


def signup(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            user.save()
            user = authenticateUser(form)
            if user is not None:
                login(request, user)
                return redirect('/dashboard/')
        else:
            return render(request, 'signup.html', {'form': form})

    return render(request, 'signup.html', {'form': SignUpForm()})


@require_POST
def projects(request):
    form = request.POST

    if 'add_project' in form:
        if not validateProjectName(request, form):
            return redirect(request.META['HTTP_REFERER'])
        Project.objects.create(
            name=form.get('new_project_name'),
            user=request.user
        )
    if 'edit_project' in form:

        if not _validateProjectName(form) or not _validateProjectId(request, form):
            return redirect(request.META['HTTP_REFERER'])

        project = Project.objects.filter(id=form.get('project_id'))
        project.update(name=form.get('edit_project_name'))

    if 'delete_project' in form:
        if not validateProjectId(form):
            return redirect('filters', filter='today')

        project = Project.objects.filter(id=form.get('project_id'))[0]
        unfinished_tasks = project.task_set.filter(is_done=False).count()
        if unfinished_tasks > 0:
            return redirect('project', id=form.get('project_id'))
        project.delete()
    return redirect('/dashboard/')


@require_POST
def tasks(request):
    form = request.POST

    if not _validateTask(request, form):
        return redirect(request.META['HTTP_REFERER'])

    if 'add_task' in form:
        Task.objects.create(
            name=form.get('task_name'),
            project_id=form.get('project_id'),
            priority=form.get('priority'),
            acomplish_date=datetime.datetime.strptime(
                form.get('task_date'), "%Y-%m-%d")
        )

    if 'edit_task' in form:
        task = Task.objects.filter(id=form.get('task_id'))
        task.update(
            name=form.get('task_name'),
            priority=form.get('priority'),
            is_done=bool(form.get('is_done')),
            acomplish_date=datetime.datetime.strptime(
                form.get('task_date'), "%Y-%m-%d")
        )

    if 'delete_task' in form:
        Task.objects.filter(id=form.get('task_id')).delete()

    if 'archive' in request.META['HTTP_REFERER']:
        return redirect('archive')
    return redirect('filters', filter='week')


@login_required(redirect_field_name=None)
def project(request, id):
    userData = Project.objects.filter(user=request.user, id=id)
    userData.project_name = None
    for item in userData:
        if userData.project_name is None:
            userData.project_name = item.name
        item.tasks = item.task_set.filter(is_done=False)
        userData = flattenTasks(item, userData)
    return render(request, 'dashboard.html', {'userData': userData})


@login_required(redirect_field_name=None)
def archive(request):
    userData = Project.objects.filter(user=request.user)
    for item in userData:
        item.tasks = item.task_set.filter(is_done=True)
        userData = flattenTasks(item, userData)

    return render(request, 'dashboard.html', {'userData': userData, 'archive': True})


@login_required(redirect_field_name=None)
def filters(request, filter):
    userData = Project.objects.filter(user=request.user)

    today_min = datetime.datetime.combine(
        datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(
        datetime.date.today(), datetime.time.max)

    if userData:
        for item in userData:
            if filter == 'today':
                item.tasks = item.task_set.filter(
                    acomplish_date__range=(today_min, today_max),
                    is_done=False
                )
            if filter == 'week':
                item.tasks = item.task_set.filter(
                    acomplish_date__gte=datetime.date.today(),
                    acomplish_date__lte=datetime.date.today() + datetime.timedelta(days=7),
                    is_done=False
                )
            userData = flattenTasks(item, userData)
    return render(request, 'dashboard.html', {'userData': userData, 'filter': filter})


def _validateProjectId(request, form):
    return len(Project.objects.filter(user=request.user, id=form.get('project_id')))


def _validateProjectName(form):
    if 'add_project' in form:
        attr_name = 'new_project_name'
    if 'edit_project' in form:
        attr_name = 'edit_project_name'
    return len(form.get(attr_name))


def _validateTask(request, form):
    if datetime.datetime.strptime(form.get('task_date'), "%Y-%m-%d") < datetime.datetime.combine(
            datetime.date.today(), datetime.time.min):
        return False
    if 'add_task' in form and not _validateProjectId(request, form):
        return False
    if not len(form.get('task_name')):
        return False
    if int(form.get('priority')) not in (1, 2, 3):
        return False
    if 'delete_task' in form and not len(Task.objects.filter(id=form.get('task_id'))):
        return False
    return True
