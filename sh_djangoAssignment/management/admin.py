from django.contrib import admin
from .models import MalfunctionReport,ImprovementReport,InvestigateImprovement,InvestigateMalfunction
# Register your models here.
admin.site.register(MalfunctionReport)
admin.site.register(ImprovementReport)
admin.site.register(InvestigateImprovement)
admin.site.register(InvestigateMalfunction)

