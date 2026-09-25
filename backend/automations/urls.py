from django.urls import include,path
from rest_framework.routers import DefaultRouter
from .views import WorkflowViewSet,ActivityViewSet,dashboard
router=DefaultRouter()
router.register("workflows",WorkflowViewSet,basename="workflow")
router.register("activity",ActivityViewSet,basename="activity")
urlpatterns=[path("dashboard/",dashboard),path("",include(router.urls))]
