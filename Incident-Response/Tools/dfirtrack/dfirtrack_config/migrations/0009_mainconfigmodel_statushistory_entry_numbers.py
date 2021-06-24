from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dfirtrack_config', '0008_statushistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainconfigmodel',
            name='statushistory_entry_numbers',
            field=models.IntegerField(default=10),
        ),
    ]
