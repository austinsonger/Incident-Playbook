from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dfirtrack_artifacts', '0003_new_artifact_note_fields'),
        ('dfirtrack_config', '0005_new_artifact_note_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainconfigmodel',
            name='artifactstatus_open',
            field=models.ManyToManyField(blank=True, related_name='main_config_artifactstatus_open', to='dfirtrack_artifacts.Artifactstatus'),
        ),
    ]
