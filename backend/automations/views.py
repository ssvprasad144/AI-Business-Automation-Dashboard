from django.db import transaction
from django.db.models import Sum,Avg
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import api_view,action
from rest_framework.response import Response
from .models import Workflow,WorkflowStep,WorkflowExecution,ActivityEvent,AutomationEnquiry
from .serializers import WorkflowSerializer,WorkflowStepSerializer,ExecutionSerializer,ActivitySerializer,AutomationEnquirySerializer
from .services import generate_workflow_suggestion,run_lead_demo,run_support_demo,run_extraction_demo,run_message_demo

DEMO_CONFIGS={
    "lead":{"name":"AI Lead Qualification Demo","trigger":"Manual demo input","steps":["Receive enquiry","AI qualification","Prepare suggested response","Return result"]},
    "support":{"name":"AI Customer Support Demo","trigger":"Customer question","steps":["Validate question","Identify intent","Search demo knowledge base","Generate response","Return result"]},
    "extract":{"name":"AI Data Extraction Demo","trigger":"Text submission","steps":["Parse input","Extract fields","Validate fields","Return structured data"]},
    "message":{"name":"AI Message Generator Demo","trigger":"Message request","steps":["Validate request","Draft message","Quality check","Preview result"]}
}

def _demo_workflow(key):
    cfg=DEMO_CONFIGS[key]
    workflow,_=Workflow.objects.get_or_create(name=cfg["name"],defaults={"trigger":cfg["trigger"],"status":"active"})
    if workflow.status!="active":
        workflow.status="active"
        workflow.save(update_fields=["status","updated_at"])
    if not workflow.steps.exists():
        for position,name in enumerate(cfg["steps"],1):
            WorkflowStep.objects.create(workflow=workflow,name=name,action_type="ai" if "AI" in name or "Extract" in name or "Draft" in name else "log",position=position)
    return workflow

def _record_demo(workflow,input_data,result):
    execution=WorkflowExecution.objects.create(workflow=workflow,input_data=input_data)
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
    return execution

class WorkflowViewSet(viewsets.ModelViewSet):
    queryset=Workflow.objects.prefetch_related("steps").all()
    serializer_class=WorkflowSerializer
    @action(detail=True,methods=["post"],url_path="run")
    def run(self,request,pk=None):
        workflow=self.get_object()
        if workflow.status!="active": return Response({"detail":"Only active workflows can be executed."},status=400)
        execution=WorkflowExecution.objects.create(workflow=workflow,input_data=request.data or {})
        steps=list(workflow.steps.all())
        if not steps: steps=[WorkflowStep.objects.create(workflow=workflow,name="Execution recorded",action_type="log",position=1)]
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
    def get_queryset(self):
        qs=super().get_queryset()
        workflow_id=self.request.query_params.get("workflow")
        return qs.filter(workflow_id=workflow_id) if workflow_id else qs

class ExecutionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=WorkflowExecution.objects.select_related("workflow").all()
    serializer_class=ExecutionSerializer

class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=ActivityEvent.objects.select_related("workflow","execution").all()
    serializer_class=ActivitySerializer

@api_view(["GET"])
def dashboard(request):
    qs=Workflow.objects.all()
    return Response({"automations":qs.count(),"active":qs.filter(status="active").count(),"successful_runs":qs.aggregate(total=Sum("runs"))["total"] or 0,"average_success_rate":round(float(qs.aggregate(avg=Avg("success_rate"))["avg"] or 0),1),"workflows":WorkflowSerializer(qs[:10],many=True).data,"activity":ActivitySerializer(ActivityEvent.objects.select_related("workflow","execution")[:10],many=True).data,"executions":ExecutionSerializer(WorkflowExecution.objects.select_related("workflow")[:10],many=True).data})

@api_view(["POST"])
def ai_suggest(request):
    description=request.data.get("description","").strip()
    if not description:return Response({"detail":"description is required"},status=400)
    return Response(generate_workflow_suggestion(description))

@api_view(["POST"])
def demo_lead(request):
    enquiry=request.data.get("enquiry","").strip()
    if not enquiry:return Response({"detail":"enquiry is required"},status=400)
    return _run_demo("lead",{"enquiry":enquiry},run_lead_demo(enquiry))

@api_view(["POST"])
def demo_support(request):
    question=request.data.get("question","").strip()
    if not question:return Response({"detail":"question is required"},status=400)
    return _run_demo("support",{"question":question},run_support_demo(question))

@api_view(["POST"])
def demo_extract(request):
    text=request.data.get("text","").strip()
    if not text:return Response({"detail":"text is required"},status=400)
    return _run_demo("extract",{"text":text},run_extraction_demo(text))

@api_view(["POST"])
def demo_message(request):
    purpose=request.data.get("purpose","").strip()
    recipient=request.data.get("recipient","").strip()
    tone=request.data.get("tone","Professional").strip()
    context=request.data.get("context","").strip()
    if not purpose or not recipient or not context:return Response({"detail":"purpose, recipient and context are required"},status=400)
    return _run_demo("message",{"purpose":purpose,"recipient":recipient,"tone":tone,"context":context},run_message_demo(purpose,recipient,tone,context))

def _run_demo(key,input_data,result):
    workflow=_demo_workflow(key)
    execution=_record_demo(workflow,input_data,result)
    return Response({"success":True,"execution":ExecutionSerializer(execution).data,"demo":result})


@api_view(["POST"])
def automation_enquiry(request):
    serializer=AutomationEnquirySerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"detail":"Please provide a valid name, email, business process, and optional integration.","errors":serializer.errors},status=400)
    enquiry=serializer.save()
    return Response({"success":True,"message":"Enquiry received. This demo stores the request for follow-up; no external message is sent.","enquiry":AutomationEnquirySerializer(enquiry).data},status=201)
