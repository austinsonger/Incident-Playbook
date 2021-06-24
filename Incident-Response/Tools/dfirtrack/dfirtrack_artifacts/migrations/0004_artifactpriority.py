from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dfirtrack_artifacts', '0003_new_artifact_note_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artifactpriority',
            fields=[
                ('artifactpriority_id', models.AutoField(primary_key=True, serialize=False)),
                ('artifactpriority_name', models.CharField(max_length=255, unique=True)),
                ('artifactpriority_note', models.TextField(blank=True, null=True)),
                ('artifactpriority_slug', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ('artifactpriority_id',),
            },
        ),
        migrations.AddField(
            model_name='artifact',
            name='artifactpriority',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='dfirtrack_artifacts.artifactpriority'),
        ),
    ]
