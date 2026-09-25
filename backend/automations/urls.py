from django.urls import include,path
from rest_framework.routers import DefaultRouter
from .views import WorkflowViewSet,ActivityViewSet,dashboard,ai_suggest
router=DefaultRouter()
router.register("workflows",WorkflowViewSet,basename="workflow")
router.register("activity",ActivityViewSet,basename="activity")
urlpatterns=[path("dashboard/",dashboard),path("ai/suggest/",ai_suggest),path("",include(router.urls))]