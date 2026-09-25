from django.contrib import admin
from .models import Workflow,WorkflowStep,WorkflowExecution,ActivityEvent,AutomationEnquiry
admin.site.register(Workflow)
admin.site.register(WorkflowStep)
admin.site.register(WorkflowExecution)
admin.site.register(ActivityEvent)

admin.site.register(AutomationEnquiry)
