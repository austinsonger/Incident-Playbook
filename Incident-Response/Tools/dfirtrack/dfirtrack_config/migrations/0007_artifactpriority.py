from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dfirtrack_config', '0006_mainconfigmodel_artifactstatus_open'),
    ]

    operations = [
        migrations.AddField(
            model_name='artifactexporterspreadsheetxlsconfigmodel',
            name='artifactlist_xls_artifactpriority',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
