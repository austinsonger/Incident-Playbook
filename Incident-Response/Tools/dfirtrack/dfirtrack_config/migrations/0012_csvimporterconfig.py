from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dfirtrack_main', '0011_removed_nullbooleanfields'),
        ('dfirtrack_config', '0011_cron_variables'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemImporterFileCsvConfigModel',
            fields=[
                ('system_importer_file_csv_config_name', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False)),
                ('csv_column_system', models.IntegerField()),
                ('csv_skip_existing_system', models.BooleanField(blank=True)),
                ('csv_headline', models.BooleanField(blank=True)),
                ('csv_import_path', models.CharField(default='/tmp', max_length=4096)),
                ('csv_import_filename', models.CharField(default='systems.csv', max_length=255)),
                ('csv_remove_systemstatus', models.BooleanField(blank=True)),
                ('csv_remove_analysisstatus', models.BooleanField(blank=True)),
                ('csv_choice_tagfree_systemstatus', models.BooleanField(blank=True)),
                ('csv_choice_tagfree_analysisstatus', models.BooleanField(blank=True)),
                ('csv_tag_lock_systemstatus', models.CharField(default='LOCK_SYSTEMSTATUS', max_length=50)),
                ('csv_tag_lock_analysisstatus', models.CharField(default='LOCK_ANALYSISSTATUS', max_length=50)),
                ('csv_choice_ip', models.BooleanField(blank=True)),
                ('csv_column_ip', models.IntegerField(blank=True, null=True)),
                ('csv_remove_ip', models.BooleanField(blank=True)),
                ('csv_choice_dnsname', models.BooleanField(blank=True)),
                ('csv_column_dnsname', models.IntegerField(blank=True, null=True)),
                ('csv_remove_dnsname', models.BooleanField(blank=True)),
                ('csv_choice_domain', models.BooleanField(blank=True)),
                ('csv_column_domain', models.IntegerField(blank=True, null=True)),
                ('csv_remove_domain', models.BooleanField(blank=True)),
                ('csv_choice_location', models.BooleanField(blank=True)),
                ('csv_column_location', models.IntegerField(blank=True, null=True)),
                ('csv_remove_location', models.BooleanField(blank=True)),
                ('csv_choice_os', models.BooleanField(blank=True)),
                ('csv_column_os', models.IntegerField(blank=True, null=True)),
                ('csv_remove_os', models.BooleanField(blank=True)),
                ('csv_choice_reason', models.BooleanField(blank=True)),
                ('csv_column_reason', models.IntegerField(blank=True, null=True)),
                ('csv_remove_reason', models.BooleanField(blank=True)),
                ('csv_choice_recommendation', models.BooleanField(blank=True)),
                ('csv_column_recommendation', models.IntegerField(blank=True, null=True)),
                ('csv_remove_recommendation', models.BooleanField(blank=True)),
                ('csv_choice_serviceprovider', models.BooleanField(blank=True)),
                ('csv_column_serviceprovider', models.IntegerField(blank=True, null=True)),
                ('csv_remove_serviceprovider', models.BooleanField(blank=True)),
                ('csv_choice_systemtype', models.BooleanField(blank=True)),
                ('csv_column_systemtype', models.IntegerField(blank=True, null=True)),
                ('csv_remove_systemtype', models.BooleanField(blank=True)),
                ('csv_choice_case', models.BooleanField(blank=True)),
                ('csv_column_case', models.IntegerField(blank=True, null=True)),
                ('csv_remove_case', models.BooleanField(blank=True)),
                ('csv_choice_company', models.BooleanField(blank=True)),
                ('csv_column_company', models.IntegerField(blank=True, null=True)),
                ('csv_remove_company', models.BooleanField(blank=True)),
                ('csv_choice_tag', models.BooleanField(blank=True)),
                ('csv_column_tag', models.IntegerField(blank=True, null=True)),
                ('csv_remove_tag', models.CharField(choices=[('tag_remove_all', 'Remove all tags'), ('tag_remove_prefix', 'Remove tags with prefix'), ('tag_remove_none', 'Keep all tags')], default='tag_remove_prefix', max_length=50)),
                ('csv_tag_prefix', models.CharField(blank=True, default='AUTO', max_length=50, null=True)),
                ('csv_tag_prefix_delimiter', models.CharField(blank=True, choices=[('tag_prefix_underscore', 'Underscore'), ('tag_prefix_hyphen', 'Hyphen'), ('tag_prefix_period', 'Period')], default='tag_prefix_underscore', max_length=50, null=True)),
                ('csv_field_delimiter', models.CharField(choices=[('field_comma', 'Comma'), ('field_semicolon', 'Semicolon')], default='field_comma', max_length=50)),
                ('csv_text_quote', models.CharField(choices=[('text_double_quotation_marks', 'Double quotation marks'), ('text_single_quotation_marks', 'Single quotation marks')], default='text_double_quotation_marks', max_length=50)),
                ('csv_ip_delimiter', models.CharField(choices=[('ip_comma', 'Comma'), ('ip_semicolon', 'Semicolon'), ('ip_space', 'Space')], default='ip_semicolon', max_length=50)),
                ('csv_tag_delimiter', models.CharField(choices=[('tag_comma', 'Comma'), ('tag_semicolon', 'Semicolon'), ('tag_space', 'Space')], default='tag_space', max_length=50)),
                ('csv_default_analysisstatus', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='system_importer_file_csv_config_analysisstatus', to='dfirtrack_main.analysisstatus')),
                ('csv_default_case', models.ManyToManyField(blank=True, related_name='system_importer_file_csv_config_case', to='dfirtrack_main.Case')),
                ('csv_default_company', models.ManyToManyField(blank=True, related_name='system_importer_file_csv_config_company', to='dfirtrack_main.Company')),
                ('csv_default_dnsname', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='system_importer_file_csv_config_dnsname', to='dfirtrack_main.dnsname')),
                ('csv_default_domain', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='system_importer_file_csv_config_domain', to='dfirtrack_main.domain')),
                ('csv_default_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='system_importer_file_csv_config_location', to='dfirtrack_main.location')),
                ('csv_default_os', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='system_importer_file_csv_config_os', to='dfirtrack_main.os')),
                ('csv_default_reason', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='system_importer_file_csv_config_reason', to='dfirtrack_main.reason')),
                ('csv_default_recommendation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='system_importer_file_csv_config_recommendation', to='dfirtrack_main.recommendation')),
                ('csv_default_serviceprovider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='system_importer_file_csv_config_serviceprovider', to='dfirtrack_main.serviceprovider')),
                ('csv_default_systemstatus', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='system_importer_file_csv_config_systemstatus', to='dfirtrack_main.systemstatus')),
                ('csv_default_systemtype', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='system_importer_file_csv_config_systemtype', to='dfirtrack_main.systemtype')),
                ('csv_default_tag', models.ManyToManyField(blank=True, related_name='system_importer_file_csv_config_tag', to='dfirtrack_main.Tag')),
                ('csv_default_tagfree_analysisstatus', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='system_importer_file_csv_config_tagfree_analysisstatus', to='dfirtrack_main.analysisstatus')),
                ('csv_default_tagfree_systemstatus', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='system_importer_file_csv_config_tagfree_systemstatus', to='dfirtrack_main.systemstatus')),
                ('csv_import_username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='csv_import_username', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='systemimporterfilecsvconfigbasedconfigmodel',
            name='csv_default_analysisstatus',
        ),
        migrations.RemoveField(
            model_name='systemimporterfilecsvconfigbasedconfigmodel',
            name='csv_default_case',
        ),
        migrations.RemoveField(
            model_name='systemimporterfilecsvconfigbasedconfigmodel',
            name='csv_default_company',
        ),
        migrations.RemoveField(
            model_name='systemimporterfilecsvconfigbasedconfigmodel',
            name='csv_default_dnsname',
        ),
        migrations.RemoveField(
            model_name='systemimporterfilecsvconfigbasedconfigmodel',
            name='csv_default_domain',
        ),
        migrations.RemoveField(
            model_name='systemimporterfilecsvconfigbasedconfigmodel',
            name='csv_default_location',
        ),
        migrations.RemoveField(
            model_name='systemimporterfilecsvconfigbasedconfigmodel',
            name='csv_default_os',
        ),
        migrations.RemoveField(
            model_name='systemimporterfilecsvconfigbasedconfigmodel',
            name='csv_default_reason',
        ),
        migrations.RemoveField(
            model_name='systemimporterfilecsvconfigbasedconfigmodel',
            name='csv_default_serviceprovider',
        ),
        migrations.RemoveField(
            model_name='systemimporterfilecsvconfigbasedconfigmodel',
            name='csv_default_systemstatus',
        ),
        migrations.RemoveField(
            model_name='systemimporterfilecsvconfigbasedconfigmodel',
            name='csv_default_systemtype',
        ),
        migrations.RemoveField(
            model_name='systemimporterfilecsvconfigbasedconfigmodel',
            name='csv_default_tag',
        ),
        migrations.DeleteModel(
            name='SystemImporterFileCsvFormbasedConfigModel',
        ),
        migrations.DeleteModel(
            name='SystemImporterFileCsvConfigbasedConfigModel',
        ),
    ]
