from django.db.models import Sum,Avg
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import api_view,action
from rest_framework.response import Response
from .models import Workflow,ActivityEvent,WorkflowStep,WorkflowExecution
from .serializers import WorkflowSerializer,ActivitySerializer,WorkflowStepSerializer,ExecutionSerializer
from .services import generate_workflow_suggestion,run_lead_demo

class WorkflowViewSet(viewsets.ModelViewSet):
    queryset=Workflow.objects.all()
    serializer_class=WorkflowSerializer

    @action(detail=True, methods=["post"], url_path="run")
    def run(self, request, pk=None):
        workflow=self.get_object()
        if workflow.status != "active":
            return Response({"detail":"Only active workflows can be executed."}, status=400)
        execution=WorkflowExecution.objects.create(workflow=workflow,input_data=request.data or {})
        completed=[]
        steps=list(workflow.steps.all())
        if not steps:
            steps=[WorkflowStep.objects.create(workflow=workflow,name="Execution recorded",action_type="log",position=1)]
        for step in steps:
            ActivityEvent.objects.create(workflow=workflow,execution=execution,message=f"Step {step.position}: {step.name} completed")
            completed.append({"name":step.name,"action_type":step.action_type,"position":step.position,"status":"completed"})
        workflow.runs += 1
        previous=float(workflow.success_rate)
        workflow.success_rate=round(((previous*(workflow.runs-1))+100)/workflow.runs,2)
        workflow.save(update_fields=["runs","success_rate","updated_at"])
        step_events=[]
        steps=workflow.steps.all()
        if not steps.exists():
            steps=WorkflowStep.objects.create(workflow=workflow,name="Execution recorded",action_type="log",position=1),
        for step in steps:
            step_events.append(ActivityEvent.objects.create(workflow=workflow,message=f"Step {step.position}: {step.name} completed"))
        event=ActivityEvent.objects.create(workflow=workflow,message=f"Workflow executed successfully — run #{workflow.runs}")
        return Response({"success":True,"workflow":WorkflowSerializer(workflow).data,"steps":[{"name":s.name,"action_type":s.action_type,"position":s.position,"status":"completed"} for s in steps],"activity":ActivitySerializer(event).data})

class WorkflowStepViewSet(viewsets.ModelViewSet):
    queryset=WorkflowStep.objects.select_related("workflow").all()
    serializer_class=WorkflowStepSerializer

class ExecutionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=WorkflowExecution.objects.select_related("workflow").all()
    serializer_class=ExecutionSerializer

class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=ActivityEvent.objects.select_related("workflow").all()
    serializer_class=ActivitySerializer

@api_view(["GET"])
def dashboard(request):
    qs=Workflow.objects.all()
    return Response({"automations":qs.count(),"active":qs.filter(status="active").count(),"successful_runs":qs.aggregate(total=Sum("runs"))["total"] or 0,"average_success_rate":round(float(qs.aggregate(avg=Avg("success_rate"))["avg"] or 0),1),"workflows":WorkflowSerializer(qs[:10],many=True).data,"activity":ActivitySerializer(ActivityEvent.objects.select_related("workflow")[:10],many=True).data})

@api_view(["POST"])
def ai_suggest(request):
    description=request.data.get("description","").strip()
    if not description:return Response({"detail":"description is required"},status=400)
    return Response(generate_workflow_suggestion(description))