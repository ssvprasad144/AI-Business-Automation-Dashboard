from django.db.models import Sum,Avg
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import api_view,action
from rest_framework.response import Response
from .models import Workflow,WorkflowStep,WorkflowExecution,ActivityEvent
from .serializers import WorkflowSerializer,WorkflowStepSerializer,ExecutionSerializer,ActivitySerializer
from .services import generate_workflow_suggestion,run_lead_demo

class WorkflowViewSet(viewsets.ModelViewSet):
    queryset=Workflow.objects.prefetch_related("steps").all()
    serializer_class=WorkflowSerializer

    @action(detail=True,methods=["post"],url_path="run")
    def run(self,request,pk=None):
        workflow=self.get_object()
        if workflow.status!="active":
            return Response({"detail":"Only active workflows can be executed."},status=400)
        execution=WorkflowExecution.objects.create(workflow=workflow,input_data=request.data or {})
        steps=list(workflow.steps.all())
        if not steps:
            steps=[WorkflowStep.objects.create(workflow=workflow,name="Execution recorded",action_type="log",position=1)]
        completed=[]
        for step in steps:
            ActivityEvent.objects.create(workflow=workflow,execution=execution,message=f"Step {step.position}: {step.name} completed")
            completed.append({"name":step.name,"action_type":step.action_type,"position":step.position,"status":"completed"})
        workflow.runs+=1
        workflow.success_rate=round(((float(workflow.success_rate)*max(workflow.runs-1,0))+100)/workflow.runs,2)
        workflow.save(update_fields=["runs","success_rate","updated_at"])
        execution.status="success"
        execution.output_data={"steps":completed,"message":"Workflow completed successfully."}
        execution.finished_at=timezone.now()
        execution.save(update_fields=["status","output_data","finished_at"])
        event=ActivityEvent.objects.create(workflow=workflow,execution=execution,message=f"Workflow completed successfully — run #{workflow.runs}")
        return Response({"success":True,"execution":ExecutionSerializer(execution).data,"activity":ActivitySerializer(event).data})

class WorkflowStepViewSet(viewsets.ModelViewSet):
    queryset=WorkflowStep.objects.select_related("workflow").all()
    serializer_class=WorkflowStepSerializer

class ExecutionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=WorkflowExecution.objects.select_related("workflow").all()
    serializer_class=ExecutionSerializer

class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=ActivityEvent.objects.select_related("workflow","execution").all()
    serializer_class=ActivitySerializer

@api_view(["GET"])
def dashboard(request):
    qs=Workflow.objects.all()
    return Response({
        "automations":qs.count(),
        "active":qs.filter(status="active").count(),
        "successful_runs":qs.aggregate(total=Sum("runs"))["total"] or 0,
        "average_success_rate":round(float(qs.aggregate(avg=Avg("success_rate"))["avg"] or 0),1),
        "workflows":WorkflowSerializer(qs[:10],many=True).data,
        "activity":ActivitySerializer(ActivityEvent.objects.select_related("workflow","execution")[:10],many=True).data,
        "executions":ExecutionSerializer(WorkflowExecution.objects.select_related("workflow")[:10],many=True).data
    })

@api_view(["POST"])
def ai_suggest(request):
    description=request.data.get("description","").strip()
    if not description:return Response({"detail":"description is required"},status=400)
    return Response(generate_workflow_suggestion(description))

@api_view(["POST"])
def demo_lead(request):
    enquiry=request.data.get("enquiry","").strip()
    if not enquiry:return Response({"detail":"enquiry is required"},status=400)
    workflow,_=Workflow.objects.get_or_create(
        name="AI Lead Qualification Demo",
        defaults={"trigger":"Manual demo input","status":"active"}
    )
    if not workflow.steps.exists():
        for position,name,action_type in [
            (1,"Receive enquiry","log"),
            (2,"AI qualification","ai"),
            (3,"Prepare suggested response","transform"),
            (4,"Return result","log")
        ]:
            WorkflowStep.objects.create(workflow=workflow,name=name,action_type=action_type,position=position)
    execution=WorkflowExecution.objects.create(workflow=workflow,input_data={"enquiry":enquiry})
    result=run_lead_demo(enquiry)
    execution.status="success"
    execution.output_data=result
    execution.finished_at=timezone.now()
    execution.save(update_fields=["status","output_data","finished_at"])
    workflow.runs+=1
    workflow.success_rate=round(((float(workflow.success_rate)*max(workflow.runs-1,0))+100)/workflow.runs,2)
    workflow.save(update_fields=["runs","success_rate","updated_at"])
    for step in workflow.steps.all():
        ActivityEvent.objects.create(workflow=workflow,execution=execution,message=f"Step {step.position}: {step.name} completed")
    ActivityEvent.objects.create(workflow=workflow,execution=execution,message="Live demo completed successfully")
    return Response({"success":True,"execution":ExecutionSerializer(execution).data,"demo":result})
