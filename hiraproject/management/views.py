from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import generic, View
from .models import MalfunctionReport, ImprovementReport, InvestigateMalfunction, Task, InvestigateImprovement
from .decorators import allowed_users,staff_only,user_only


@method_decorator(user_only, name='dispatch')
class UserHomepage(LoginRequiredMixin,generic.TemplateView):
    """Home Page displayed to user for creating reports: User Method"""
    template_name = 'management/user_homepage.html'


@method_decorator(staff_only, name='dispatch')
class Homepage(LoginRequiredMixin,generic.TemplateView):
    """Staff side home page: Staff Method"""
    template_name = 'management/homepage.html'


@method_decorator(allowed_users(allowed_roles=['user']), name='dispatch')
class MalfunctionCreate(LoginRequiredMixin, generic.CreateView):
    """Creating malfunction reports: User Method"""
    model = MalfunctionReport
    fields = ['subject', 'description']
    template_name = 'management/report_createForm.html'
    success_url = reverse_lazy('management:user-homepage')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(allowed_users(allowed_roles=['user']), name='dispatch')
class ImprovementCreate(LoginRequiredMixin, generic.CreateView):
    """Creating Improvement report: User Method"""
    model = ImprovementReport
    fields = ['subject', 'description']
    template_name = 'management/report_createForm.html'
    success_url = reverse_lazy('management:user-homepage')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(allowed_users(allowed_roles=['staff']), name='dispatch')
class MalfunctionList(LoginRequiredMixin, generic.ListView):
    """Listing all malfunction reports: Staff Method"""
    queryset = MalfunctionReport.objects.all()
    context_object_name = 'malfunction_list'
    template_name = 'management/malfunction_list.html'


@method_decorator(allowed_users(allowed_roles=['staff']), name='dispatch')
class ImprovementList(generic.ListView):
    """Listing all improvement reports: Staff Method"""
    queryset = ImprovementReport.objects.all()
    context_object_name = 'improvement_list'
    template_name = 'management/improvement_list.html'


@method_decorator(allowed_users(allowed_roles=['staff']), name='dispatch')
@method_decorator(allowed_users('staff'), name='dispatch')
class MalfunctionDetail(LoginRequiredMixin, generic.DetailView):
    """Displaying detail of required report i.e. reports detail,investigation detail(if exists),
    along with task detail, Staff Method."""
    model = MalfunctionReport
    context_object_name = 'report'
    template_name = 'management/malfunction_detail.html'
    pk_url_kwarg = 'report_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = get_object_or_404(MalfunctionReport, id=self.kwargs['report_id'])
        if report.is_investigated():
            investigation_report = get_object_or_404(InvestigateMalfunction, report_id=self.kwargs['report_id'])
            context['investigation_report'] = investigation_report
            if investigation_report.is_valid:
                task = get_object_or_404(Task, investigate_id=investigation_report.id)
                context['task'] = task
        return context


@method_decorator(allowed_users(allowed_roles=['staff']), name='dispatch')
class ImprovementDetail(LoginRequiredMixin, generic.DetailView):
    """Displaying detail of required report i.e. reports detail,investigation detail(if exists) Staff Method."""
    model = ImprovementReport
    context_object_name = 'report'
    template_name = 'management/improvement_detail.html'
    pk_url_kwarg = 'report_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = get_object_or_404(ImprovementReport, id=self.kwargs['report_id'])
        if report.is_investigated():
            investigation_report = get_object_or_404(InvestigateImprovement, report_id=self.kwargs['report_id'])
            context['investigation_report'] = investigation_report
        return context


@method_decorator(allowed_users(allowed_roles=['staff']), name='dispatch')
class MalfunctionValidate(LoginRequiredMixin, generic.TemplateView):
    """Investigate current report and mark it as valid/invalid.
        Show task prompt if marked valid: Staff Method"""
    template_name = 'management/task_prompt.html'
    pk_url_kwarg = 'report_id'

    def dispatch(self, request, *args, **kwargs):
        report = get_object_or_404(MalfunctionReport, id=self.kwargs['report_id'])
        investigate_mal = InvestigateMalfunction(report_id=report)
        investigate_mal.author = self.request.user
        if not self.kwargs['validity'] == 'valid':
            investigate_mal.is_valid = False
            investigate_mal.save()
            return redirect('management:list-malfunction')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = get_object_or_404(MalfunctionReport, id=self.kwargs['report_id'])
        investigate_mal = InvestigateMalfunction(report_id=report)
        investigate_mal.is_valid = True
        investigate_mal.save()
        context['investigate_mal'] = investigate_mal
        return context


@method_decorator(allowed_users(allowed_roles=['staff']), name='dispatch')
class ImprovementValidate(LoginRequiredMixin, generic.TemplateView):
    """Investigate current report and mark it as valid/invalid: Staff Method"""

    def dispatch(self, request, *args, **kwargs):
        report = get_object_or_404(ImprovementReport, id=self.kwargs['report_id'])
        investigate_imp = InvestigateImprovement(report_id=report)
        investigate_imp.author = self.request.user
        if self.kwargs['validity'] == 'valid':
            investigate_imp.is_valid = True
        else:
            investigate_imp.is_valid = False
        investigate_imp.save()
        return redirect('management:list-improvement')


@method_decorator(allowed_users(allowed_roles=['staff']), name='dispatch')
class MalfunctionTaskCreate(LoginRequiredMixin, generic.CreateView):
    """Assigning task to any malfunction report: Staff Method"""
    model = Task
    fields = ['state', 'priority', 'time_created']
    template_name = 'management/task_createForm.html'
    success_url = reverse_lazy('management:list-malfunction')
    pk_url_kwarg = 'investigate_id'
    context_object_name = 'task'

    def form_valid(self, form):
        investigate_mal_obj = get_object_or_404(InvestigateMalfunction, id=self.kwargs['investigate_id'])
        form.instance.investigate_id = investigate_mal_obj
        return super().form_valid(form)


@method_decorator(allowed_users(allowed_roles=['staff']), name='dispatch')
class TaskCompletion(LoginRequiredMixin, generic.TemplateView):
    """Mark task as complete and save current time"""

    def dispatch(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        if task.state != 'C':
            task.state = 'C'
            task.time_completed = timezone.now()
            task.save()
        return redirect('management:list-malfunction')
