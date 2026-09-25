from django.contrib import admin
from .models import Workflow,ActivityEvent,WorkflowStep
admin.site.register(Workflow)
admin.site.register(ActivityEvent)
admin.site.register(WorkflowStep)
