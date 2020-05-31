from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import MalfunctionReport, ImprovementReport, InvestigateMalfunction, Task, InvestigateImprovement
from django.contrib.auth.decorators import login_required
from . import forms
from .decorators import allowed_users


@login_required
@allowed_users(allowed_roles=['user'])
def user_homepage(request):
    """Home Page displayed to user for creating reports: User Method"""
    return render(request, 'management/user_homepage.html')


@login_required
@allowed_users(allowed_roles=['staff'])
def homepage(request):
    """Staff side home page: Staff Method"""
    return render(request, 'management/homepage.html')


@login_required
@allowed_users(allowed_roles=['user'])
def create_malfunction(request):
    """Creating malfunction reports: User Method"""
    if request.method == 'POST':
        form = forms.MalfunctionForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            report.save()
        return redirect('/management/user/')
    else:
        form = forms.MalfunctionForm()
    return render(request, "management/report_createForm.html.html", {'form': form})


@login_required
@allowed_users(allowed_roles=['user'])
def create_improvement(request):
    """Creating Improvement report: User Method"""
    if request.method == 'POST':
        form = forms.ImprovementForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            report.save()
        return redirect('/management/user/')
    else:
        form = forms.MalfunctionForm()
    return render(request, "management/report_createForm.html.html", {'form': form})


@login_required
@allowed_users(allowed_roles=['staff'])
def list_malfunction(request):
    """Listing all malfunction reports: Staff Method"""
    malfunction_list = MalfunctionReport.objects.all()
    context = {'malfunction_list': malfunction_list}
    return render(request, 'management/malfunction_list.html', context)


@login_required
@allowed_users(allowed_roles=['staff'])
def list_improvement(request):
    """Listing all improvement reports: Staff Method"""
    improvement_list = ImprovementReport.objects.all()
    context = {'improvement_list': improvement_list}
    return render(request, 'management/improvement_list.html', context)


@login_required
@allowed_users(allowed_roles=['staff'])
def detail_malfunction(request, report_id):
    """Displaying detail of required report i.e. reports detail,investigation along with task detail(if exists). """
    
    report = get_object_or_404(MalfunctionReport, id=report_id)
    if report.is_investigated():
        investigation_report = get_object_or_404(InvestigateMalfunction, report_id=report_id)
        if investigation_report.is_valid:
            task = get_object_or_404(Task, investigate_id=investigation_report.id)
            context = {'report': report, 'investigation_report': investigation_report, 'task': task}
        else:
            context = {'report': report, 'investigation_report': investigation_report}
    else:
        context = {'report': report}
    return render(request, 'management/malfunction_detail.html', context)



@login_required
@allowed_users(allowed_roles=['staff'])
def detail_improvement(request, report_id):
    """Displaying detail of required report i.e. reports detail,investigation detail(if exists)."""
    
    report = get_object_or_404(ImprovementReport, id=report_id)
    if report.is_investigated():
        investigation_report = get_object_or_404(InvestigateImprovement, report_id=report_id)
        context = {'report': report, 'investigation_report': investigation_report}
    else:
        context = {'report': report}
    return render(request, 'management/improvement_detail.html', context)

@login_required
@allowed_users(allowed_roles=['staff'])
def validate_malfunction(request, report_id, validity):
    """Investigate current report and mark it as valid/invalid.
        Show task prompt if marked valid: Staff Method"""
    report = get_object_or_404(MalfunctionReport, id=report_id)
    investigate_mal = InvestigateMalfunction(report_id=report)
    investigate_mal.author = request.user
    if validity == 'valid':
        investigate_mal.is_valid = True
        investigate_mal.save()
        context = {'investigate_mal': investigate_mal, 'report': report}
        return render(request, 'management/task_prompt.html', context)
    else:
        investigate_mal.is_valid = False
        investigate_mal.save()
        return redirect('/management/malfunction_reports/')


@login_required
@allowed_users(allowed_roles=['staff'])
def validate_improvement(request, report_id, validity):
    """Investigate current report and mark it as valid/invalid: Staff Method"""
    report = get_object_or_404(ImprovementReport, id=report_id)
    investigate_imp = InvestigateImprovement(report_id=report)
    if validity == 'valid':
        investigate_imp.is_valid = True
    else:
        investigate_imp.is_valid = False
    investigate_imp.author = request.user
    investigate_imp.save()
    return redirect('/management/improvement_reports/')


@login_required
@allowed_users(allowed_roles=['staff'])
def create_malfunction_task(request, investigate_id):
    """Assigning task to any malfunction report: Staff Method"""
    if request.method == 'POST':
        form = forms.TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            investigate_mal_obj = get_object_or_404(InvestigateMalfunction, id=investigate_id)
            task.investigate_id = investigate_mal_obj
            task.save()
        return redirect('/management/malfunction_reports/')
    else:
        form = forms.TaskForm()
    return render(request, "management/task_createForm.html", {'form': form})


@login_required
@allowed_users(allowed_roles=['staff'])
def task_completion(request, task_id):
    """Mark task as complete and save current time"""
    task = get_object_or_404(Task, id=task_id)
    task.state = 'C'
    task.time_completed = timezone.now()
    task.save()
    return redirect('/management/malfunction_reports/')