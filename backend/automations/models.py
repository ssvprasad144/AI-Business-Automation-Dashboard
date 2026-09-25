from django.db import models
class Workflow(models.Model):
    STATUS_CHOICES=[("active","Active"),("paused","Paused"),("draft","Draft")]
    name=models.CharField(max_length=160)
    trigger=models.CharField(max_length=200)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="draft")
    runs=models.PositiveIntegerField(default=0)
    success_rate=models.DecimalField(max_digits=5,decimal_places=2,default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=["-updated_at"]
    def __str__(self): return self.name
class ActivityEvent(models.Model):
    workflow=models.ForeignKey(Workflow,on_delete=models.CASCADE,related_name="events")
    message=models.CharField(max_length=240)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["-created_at"]

class WorkflowStep(models.Model):
    ACTION_CHOICES=[("ai","AI Process"),("webhook","Webhook"),("email","Email"),("transform","Transform"),("log","Log")]
    workflow=models.ForeignKey(Workflow,on_delete=models.CASCADE,related_name="steps")
    name=models.CharField(max_length=160)
    action_type=models.CharField(max_length=30,choices=ACTION_CHOICES,default="ai")
    position=models.PositiveIntegerField(default=1)
    config=models.JSONField(default=dict,blank=True)
    class Meta:
        ordering=["position","id"]
    def __str__(self): return f"{self.workflow.name} · {self.name}"
