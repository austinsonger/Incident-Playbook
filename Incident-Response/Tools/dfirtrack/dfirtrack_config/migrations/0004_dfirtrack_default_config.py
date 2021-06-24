from django.db import migrations
from dfirtrack import settings

class Migration(migrations.Migration):

    dependencies = [
        ('dfirtrack_config', '0003_dfirtrack_config'),
    ]

    # PostgreSQL (uses TRUE / FALSE as boolean)
    if settings.DATABASES['default']['ENGINE'].split('.')[-1] == 'postgresql':

        operations = [

            migrations.RunSQL("INSERT INTO dfirtrack_config_mainconfigmodel (main_config_name, system_name_editable) VALUES ('MainConfig', FALSE);"),

        ]

    # SQLite3 (uses 1 / 0 as boolean)
    else:       # coverage: ignore branch

        operations = [

            migrations.RunSQL("INSERT INTO dfirtrack_config_mainconfigmodel (main_config_name, system_name_editable) VALUES ('MainConfig', 0);"),

        ]
