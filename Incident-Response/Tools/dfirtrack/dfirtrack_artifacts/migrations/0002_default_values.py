from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('dfirtrack_artifacts', '0001_initial'),
    ]

    operations = [

        migrations.RunSQL("INSERT INTO dfirtrack_artifacts_artifactstatus (artifactstatus_name, artifactstatus_slug) VALUES ('10_needs_analysis', '10_needs_analysis');"),
        migrations.RunSQL("INSERT INTO dfirtrack_artifacts_artifactstatus (artifactstatus_name, artifactstatus_slug) VALUES ('20_requested', '20_requested');"),
        migrations.RunSQL("INSERT INTO dfirtrack_artifacts_artifactstatus (artifactstatus_name, artifactstatus_slug) VALUES ('21_requested_again', '21_requested_again');"),
        migrations.RunSQL("INSERT INTO dfirtrack_artifacts_artifactstatus (artifactstatus_name, artifactstatus_slug) VALUES ('25_collection_ongoing', '25_collection_ongoing');"),
        migrations.RunSQL("INSERT INTO dfirtrack_artifacts_artifactstatus (artifactstatus_name, artifactstatus_slug) VALUES ('30_processing_ongoing', '30_processing_ongoing');"),
        migrations.RunSQL("INSERT INTO dfirtrack_artifacts_artifactstatus (artifactstatus_name, artifactstatus_slug) VALUES ('40_import_ongoing', '40_import_ongoing');"),
        migrations.RunSQL("INSERT INTO dfirtrack_artifacts_artifactstatus (artifactstatus_name, artifactstatus_slug) VALUES ('50_ready_for_analysis', '50_ready_for_analysis');"),
        migrations.RunSQL("INSERT INTO dfirtrack_artifacts_artifactstatus (artifactstatus_name, artifactstatus_slug) VALUES ('60_analysis_ongoing', '60_analysis_ongoing');"),
        migrations.RunSQL("INSERT INTO dfirtrack_artifacts_artifactstatus (artifactstatus_name, artifactstatus_slug) VALUES ('70_analysis_finished', '70_analysis_finished');"),
        migrations.RunSQL("INSERT INTO dfirtrack_artifacts_artifactstatus (artifactstatus_name, artifactstatus_slug) VALUES ('90_not_analyzed', '90_not_analyzed');"),
        migrations.RunSQL("INSERT INTO dfirtrack_artifacts_artifactstatus (artifactstatus_name, artifactstatus_slug) VALUES ('95_not_available', '95_not_available');"),

        migrations.RunSQL("INSERT INTO dfirtrack_artifacts_artifacttype (artifacttype_name, artifacttype_slug) VALUES ('File', 'file');"),
        migrations.RunSQL("INSERT INTO dfirtrack_artifacts_artifacttype (artifacttype_name, artifacttype_slug) VALUES ('Image', 'image');"),
        migrations.RunSQL("INSERT INTO dfirtrack_artifacts_artifacttype (artifacttype_name, artifacttype_slug) VALUES ('Information', 'information');"),
        migrations.RunSQL("INSERT INTO dfirtrack_artifacts_artifacttype (artifacttype_name, artifacttype_slug) VALUES ('Triage', 'triage');"),

    ]
