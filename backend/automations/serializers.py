from rest_framework import serializers
from .models import Workflow,ActivityEvent,WorkflowStep
class WorkflowSerializer(serializers.ModelSerializer):
    success=serializers.SerializerMethodField()
    class Meta:
        model=Workflow
        fields=["id","name","trigger","runs","status","success","created_at","updated_at"]
    def get_success(self,obj): return f"{obj.success_rate:g}%"
class ActivitySerializer(serializers.ModelSerializer):
    workflow=serializers.CharField(source="workflow.name",read_only=True)
    class Meta:
        model=ActivityEvent
        fields=["id","workflow","message","created_at"]

class WorkflowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model=WorkflowStep
        fields=["id","workflow","name","action_type","position","config"]
