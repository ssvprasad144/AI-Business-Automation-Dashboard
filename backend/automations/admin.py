from django.contrib import admin
from .models import Workflow,WorkflowStep,WorkflowExecution,ActivityEvent
admin.site.register(Workflow)
admin.site.register(WorkflowStep)
admin.site.register(WorkflowExecution)
admin.site.register(ActivityEvent)
