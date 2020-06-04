from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Reports(models.Model):
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    subject = models.CharField(max_length=80)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)


class MalfunctionReport(Reports):
    def is_investigated(self):
        is_investigated = False
        try:
            is_investigated = (self.mal_investigate is not None)
        except InvestigateMalfunction.DoesNotExist:
            pass
        return is_investigated


class ImprovementReport(Reports):

    def is_investigated(self):
        is_investigated = False
        try:
            is_investigated = (self.imp_investigate is not None)
        except InvestigateImprovement.DoesNotExist:
            pass
        return is_investigated


class Investigate(models.Model):
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    is_valid = models.BooleanField(default=True)


class InvestigateMalfunction(Investigate):
    report_id = models.OneToOneField('MalfunctionReport', related_name="mal_investigate", on_delete=models.CASCADE)

    def has_assigned_task(self):
        assigned_task = False
        try:
            assigned_task = (self.mal_task is not None)
        except Task.DoesNotExist:
            pass
        return assigned_task


class InvestigateImprovement(Investigate):
    report_id = models.OneToOneField('ImprovementReport', related_name='imp_investigate', on_delete=models.CASCADE)


class Task(models.Model):
    STATE_OPTIONS = (
        ('P', 'Pending'),
        ('S', 'Started'),
        ('C', 'Complete'),
    )
    PRIORITY_OPTIONS = (
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    )
    state = models.CharField(max_length=1, choices=STATE_OPTIONS)
    investigate_id = models.OneToOneField('InvestigateMalfunction', related_name="mal_task", on_delete=models.CASCADE)
    time_created = models.DateTimeField(default=timezone.now)
    time_completed = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS)
