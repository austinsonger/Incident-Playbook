from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dfirtrack_config', '0007_artifactpriority'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statushistory',
            fields=[
                ('statushistory_id', models.AutoField(primary_key=True, serialize=False)),
                ('statushistory_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='StatushistoryEntry',
            fields=[
                ('statushistoryentry_id', models.AutoField(primary_key=True, serialize=False)),
                ('statushistoryentry_model_name', models.CharField(editable=False, max_length=255)),
                ('statushistoryentry_model_key', models.CharField(blank=True, editable=False, max_length=255)),
                ('statushistoryentry_model_value', models.IntegerField(editable=False)),
                ('statushistory', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='dfirtrack_config.Statushistory')),
            ],
        ),
    ]
