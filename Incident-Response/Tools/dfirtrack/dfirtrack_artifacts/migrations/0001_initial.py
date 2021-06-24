from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dfirtrack_main', '0009_export_attribute'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artifact',
            fields=[
                ('artifact_id', models.AutoField(primary_key=True, serialize=False)),
                ('artifact_acquisition_time', models.DateTimeField(blank=True, null=True)),
                ('artifact_md5', models.CharField(blank=True, max_length=32, null=True)),
                ('artifact_name', models.CharField(max_length=4096)),
                ('artifact_note', models.TextField(blank=True, null=True)),
                ('artifact_requested_time', models.DateTimeField(blank=True, null=True)),
                ('artifact_sha1', models.CharField(blank=True, max_length=40, null=True)),
                ('artifact_sha256', models.CharField(blank=True, max_length=64, null=True)),
                ('artifact_slug', models.CharField(max_length=4096)),
                ('artifact_source_path', models.CharField(blank=True, max_length=4096, null=True)),
                ('artifact_storage_path', models.CharField(max_length=4096, unique=True)),
                ('artifact_uuid', models.UUIDField(editable=False)),
                ('artifact_create_time', models.DateTimeField(auto_now_add=True)),
                ('artifact_modify_time', models.DateTimeField(auto_now=True)),
                ('artifact_created_by_user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='artifact_created_by', to=settings.AUTH_USER_MODEL)),
                ('artifact_modified_by_user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='artifact_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('artifact_name',),
            },
        ),
        migrations.CreateModel(
            name='Artifactstatus',
            fields=[
                ('artifactstatus_id', models.AutoField(primary_key=True, serialize=False)),
                ('artifactstatus_name', models.CharField(max_length=255, unique=True)),
                ('artifactstatus_note', models.TextField(blank=True, null=True)),
                ('artifactstatus_slug', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ('artifactstatus_id',),
            },
        ),
        migrations.CreateModel(
            name='Artifacttype',
            fields=[
                ('artifacttype_id', models.AutoField(primary_key=True, serialize=False)),
                ('artifacttype_name', models.CharField(max_length=255, unique=True)),
                ('artifacttype_note', models.TextField(blank=True, null=True)),
                ('artifacttype_slug', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ('artifacttype_id',),
            },
        ),
        migrations.AddField(
            model_name='artifact',
            name='artifactstatus',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='dfirtrack_artifacts.Artifactstatus'),
        ),
        migrations.AddField(
            model_name='artifact',
            name='artifacttype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dfirtrack_artifacts.Artifacttype'),
        ),
        migrations.AddField(
            model_name='artifact',
            name='case',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='artifact_case', to='dfirtrack_main.Case'),
        ),
        migrations.AddField(
            model_name='artifact',
            name='system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='artifact_system', to='dfirtrack_main.System'),
        ),
    ]
