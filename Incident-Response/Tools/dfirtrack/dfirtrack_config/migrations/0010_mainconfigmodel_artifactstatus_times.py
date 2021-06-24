from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dfirtrack_artifacts', '0005_values_artifactpriority'),
        ('dfirtrack_config', '0009_mainconfigmodel_statushistory_entry_numbers'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainconfigmodel',
            name='artifactstatus_acquisition',
            field=models.ManyToManyField(blank=True, related_name='main_config_artifactstatus_acquisition', to='dfirtrack_artifacts.Artifactstatus'),
        ),
        migrations.AddField(
            model_name='mainconfigmodel',
            name='artifactstatus_requested',
            field=models.ManyToManyField(blank=True, related_name='main_config_artifactstatus_requested', to='dfirtrack_artifacts.Artifactstatus'),
        ),
    ]
