from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('dfirtrack_artifacts', '0004_artifactpriority'),
    ]

    operations = [

        migrations.RunSQL("INSERT INTO dfirtrack_artifacts_artifactpriority (artifactpriority_name, artifactpriority_slug) VALUES ('10_low', '10_low');"),
        migrations.RunSQL("INSERT INTO dfirtrack_artifacts_artifactpriority (artifactpriority_name, artifactpriority_slug) VALUES ('20_medium', '20_medium');"),
        migrations.RunSQL("INSERT INTO dfirtrack_artifacts_artifactpriority (artifactpriority_name, artifactpriority_slug) VALUES ('30_high', '30_high');"),

    ]
