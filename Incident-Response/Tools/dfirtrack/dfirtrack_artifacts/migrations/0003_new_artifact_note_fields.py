from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dfirtrack_artifacts', '0002_default_values'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artifact',
            name='artifact_note',
        ),
        migrations.AddField(
            model_name='artifact',
            name='artifact_note_analysisresult',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='artifact',
            name='artifact_note_external',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='artifact',
            name='artifact_note_internal',
            field=models.TextField(blank=True, null=True),
        ),
    ]
