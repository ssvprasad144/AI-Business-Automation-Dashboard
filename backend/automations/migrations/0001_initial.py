from django.db import migrations,models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial=True
    dependencies=[]
    operations=[
        migrations.CreateModel(
            name="Workflow",
            fields=[
                ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
                ("name",models.CharField(max_length=160)),
                ("trigger",models.CharField(max_length=200)),
                ("status",models.CharField(choices=[("active","Active"),("paused","Paused"),("draft","Draft")],default="draft",max_length=20)),
                ("runs",models.PositiveIntegerField(default=0)),
                ("success_rate",models.DecimalField(decimal_places=2,default=0,max_digits=5)),
                ("created_at",models.DateTimeField(auto_now_add=True)),
                ("updated_at",models.DateTimeField(auto_now=True)),
            ],
            options={"ordering":["-updated_at"]},
        ),
        migrations.CreateModel(
            name="ActivityEvent",
            fields=[
                ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
                ("message",models.CharField(max_length=240)),
                ("created_at",models.DateTimeField(auto_now_add=True)),
                ("workflow",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="events",to="automations.workflow")),
            ],
            options={"ordering":["-created_at"]},
        ),
    ]