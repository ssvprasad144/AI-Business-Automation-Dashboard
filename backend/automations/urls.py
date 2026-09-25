from django.urls import include,path
from rest_framework.routers import DefaultRouter
from .views import WorkflowViewSet,WorkflowStepViewSet,ExecutionViewSet,ActivityViewSet,dashboard,ai_suggest,demo_lead
router=DefaultRouter()
router.register("workflows",WorkflowViewSet,basename="workflow")
router.register("steps",WorkflowStepViewSet,basename="step")
router.register("executions",ExecutionViewSet,basename="execution")
router.register("activity",ActivityViewSet,basename="activity")
urlpatterns=[path("dashboard/",dashboard),path("ai/suggest/",ai_suggest),path("demo/lead/",demo_lead),path("",include(router.urls))]
