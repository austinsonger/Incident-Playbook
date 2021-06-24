from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dfirtrack_config', '0004_dfirtrack_default_config'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artifactexporterspreadsheetxlsconfigmodel',
            name='artifactlist_xls_artifact_note',
        ),
        migrations.AddField(
            model_name='artifactexporterspreadsheetxlsconfigmodel',
            name='artifactlist_xls_artifact_note_analysisresult',
            field=models.BooleanField(blank=True, default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artifactexporterspreadsheetxlsconfigmodel',
            name='artifactlist_xls_artifact_note_external',
            field=models.BooleanField(blank=True, default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artifactexporterspreadsheetxlsconfigmodel',
            name='artifactlist_xls_artifact_note_internal',
            field=models.BooleanField(blank=True, default=False),
            preserve_default=False,
        ),
    ]
