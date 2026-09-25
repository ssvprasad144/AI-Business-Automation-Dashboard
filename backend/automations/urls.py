from django.urls import include,path
from rest_framework.routers import DefaultRouter
from .views import WorkflowViewSet,WorkflowStepViewSet,ExecutionViewSet,ActivityViewSet,dashboard,ai_suggest,demo_lead,demo_support,demo_extract,demo_message,automation_enquiry,health
router=DefaultRouter()
router.register("workflows",WorkflowViewSet,basename="workflow")
router.register("steps",WorkflowStepViewSet,basename="step")
router.register("executions",ExecutionViewSet,basename="execution")
router.register("activity",ActivityViewSet,basename="activity")
urlpatterns=[path("health/",health),path("dashboard/",dashboard),path("ai/suggest/",ai_suggest),path("demo/lead/",demo_lead),path("demo/support/",demo_support),path("demo/extract/",demo_extract),path("demo/message/",demo_message),path("enquiry/",automation_enquiry),path("",include(router.urls))]
