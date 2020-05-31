from django import forms
from . import models


class MalfunctionForm(forms.ModelForm):
    class Meta:
        model = models.MalfunctionReport
        fields = ['subject','description' ]


class ImprovementForm(forms.ModelForm):
    class Meta:
        model = models.ImprovementReport
        fields = ['subject','description']


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ['state','priority' ,'time_created']