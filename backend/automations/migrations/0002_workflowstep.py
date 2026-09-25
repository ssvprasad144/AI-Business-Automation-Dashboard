from django.db import migrations,models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies=[("automations","0001_initial")]
    operations=[
        migrations.CreateModel(
            name="WorkflowStep",
            fields=[
                ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
                ("name",models.CharField(max_length=160)),
                ("action_type",models.CharField(choices=[("ai","AI Process"),("webhook","Webhook"),("email","Email"),("transform","Transform"),("log","Log")],default="ai",max_length=30)),
                ("position",models.PositiveIntegerField(default=1)),
                ("config",models.JSONField(blank=True,default=dict)),
                ("workflow",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="steps",to="automations.workflow")),
            ],
            options={"ordering":["position","id"]},
        )
    ]
