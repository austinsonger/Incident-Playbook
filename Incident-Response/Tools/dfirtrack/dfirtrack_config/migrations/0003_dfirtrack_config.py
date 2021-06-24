from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dfirtrack_config', '0002_default_config'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainConfigModel',
            fields=[
                ('main_config_name', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False)),
                ('system_name_editable', models.BooleanField(blank=True)),
            ],
        ),
    ]
