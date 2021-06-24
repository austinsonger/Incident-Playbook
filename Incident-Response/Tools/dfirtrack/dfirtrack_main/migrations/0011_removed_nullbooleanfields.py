from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dfirtrack_main', '0010_status_history_for_system'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainuser',
            name='domainuser_is_domainadmin',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='system',
            name='system_is_vm',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='systemuser',
            name='systemuser_is_systemadmin',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
