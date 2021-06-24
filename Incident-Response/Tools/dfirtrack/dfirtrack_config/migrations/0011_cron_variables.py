from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dfirtrack_config', '0010_mainconfigmodel_artifactstatus_times'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainconfigmodel',
            name='cron_export_path',
            field=models.CharField(default='/tmp', max_length=4096),
        ),
        migrations.AddField(
            model_name='mainconfigmodel',
            name='cron_username',
            field=models.CharField(default='cron', max_length=255),
        ),
    ]
