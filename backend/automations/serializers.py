from rest_framework import serializers
from .models import Workflow,WorkflowStep,WorkflowExecution,ActivityEvent

class WorkflowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model=WorkflowStep
        fields=["id","workflow","name","action_type","position","config"]

class WorkflowSerializer(serializers.ModelSerializer):
    success=serializers.SerializerMethodField()
    steps=WorkflowStepSerializer(many=True,read_only=True)
    class Meta:
        model=Workflow
        fields=["id","name","trigger","runs","status","success","steps","created_at","updated_at"]
    def get_success(self,obj): return f"{obj.success_rate:g}%"

class ExecutionSerializer(serializers.ModelSerializer):
    workflow=serializers.CharField(source="workflow.name",read_only=True)
    class Meta:
        model=WorkflowExecution
        fields=["id","workflow","status","input_data","output_data","error","started_at","finished_at"]

class ActivitySerializer(serializers.ModelSerializer):
    workflow=serializers.CharField(source="workflow.name",read_only=True)
    class Meta:
        model=ActivityEvent
        fields=["id","workflow","execution","message","created_at"]
