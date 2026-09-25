from django.db import migrations,models

class Migration(migrations.Migration):
    dependencies=[("automations","0003_execution")]
    operations=[migrations.CreateModel(name="AutomationEnquiry",fields=[
        ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
        ("name",models.CharField(max_length=120)),
        ("email",models.EmailField(max_length=254)),
        ("business_process",models.TextField(max_length=2000)),
        ("integration",models.CharField(blank=True,max_length=120)),
        ("created_at",models.DateTimeField(auto_now_add=True)),
    ],options={"ordering":["-created_at"]})]
