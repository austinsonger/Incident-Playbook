from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dfirtrack_main', '0007_systemstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dnsname',
            fields=[
                ('dnsname_id', models.AutoField(primary_key=True, serialize=False)),
                ('dnsname_name', models.CharField(max_length=100, unique=True)),
                ('dnsname_note', models.TextField(blank=True, null=True)),
                ('domain', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dfirtrack_main.Domain')),
            ],
        ),
        migrations.CreateModel(
            name='Domainuser',
            fields=[
                ('domainuser_id', models.AutoField(primary_key=True, serialize=False)),
                ('domainuser_name', models.CharField(max_length=50)),
                ('domainuser_is_domainadmin', models.NullBooleanField()),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dfirtrack_main.Domain')),
            ],
        ),
        migrations.RemoveField(
            model_name='system',
            name='system_dnssuffix',
        ),
        migrations.AddField(
            model_name='systemuser',
            name='systemuser_is_systemadmin',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='domainuser',
            name='system_was_logged_on',
            field=models.ManyToManyField(blank=True, to='dfirtrack_main.System'),
        ),
        migrations.AddField(
            model_name='system',
            name='dnsname',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dfirtrack_main.Dnsname'),
        ),
        migrations.AlterUniqueTogether(
            name='domainuser',
            unique_together={('domain', 'domainuser_name')},
        ),
    ]
