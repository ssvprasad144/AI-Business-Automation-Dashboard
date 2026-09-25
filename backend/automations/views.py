from django.db.models import Sum,Avg
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Workflow,ActivityEvent
from .serializers import WorkflowSerializer,ActivitySerializer
class WorkflowViewSet(viewsets.ModelViewSet):
    queryset=Workflow.objects.all()
    serializer_class=WorkflowSerializer
class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=ActivityEvent.objects.select_related("workflow").all()
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
        "activity":ActivitySerializer(ActivityEvent.objects.select_related("workflow")[:10],many=True).data,
    })
