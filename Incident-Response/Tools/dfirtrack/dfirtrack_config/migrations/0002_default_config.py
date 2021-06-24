from django.db import migrations
from dfirtrack import settings

class Migration(migrations.Migration):

    dependencies = [
        ('dfirtrack_config', '0001_initial'),
    ]

    # PostgreSQL (uses TRUE / FALSE as boolean)
    if settings.DATABASES['default']['ENGINE'].split('.')[-1] == 'postgresql':

        operations = [

            migrations.RunSQL("INSERT INTO dfirtrack_config_artifactexporterspreadsheetxlsconfigmodel (artifact_exporter_spreadsheet_xls_config_name, artifactlist_xls_artifact_id, artifactlist_xls_system_id, artifactlist_xls_system_name, artifactlist_xls_artifactstatus, artifactlist_xls_artifacttype, artifactlist_xls_artifact_source_path, artifactlist_xls_artifact_storage_path, artifactlist_xls_artifact_note, artifactlist_xls_artifact_md5, artifactlist_xls_artifact_sha1, artifactlist_xls_artifact_sha256, artifactlist_xls_artifact_create_time, artifactlist_xls_artifact_modify_time, artifactlist_xls_worksheet_artifactstatus, artifactlist_xls_worksheet_artifacttype) VALUES ('ArtifactExporterSpreadsheetXlsConfig', TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, TRUE, TRUE);"),

            migrations.RunSQL("INSERT INTO dfirtrack_config_systemexportermarkdownconfigmodel (system_exporter_markdown_config_name, markdown_sorting) VALUES ('SystemExporterMarkdownConfig', 'sys');"),

            migrations.RunSQL("INSERT INTO dfirtrack_config_systemexporterspreadsheetcsvconfigmodel (system_exporter_spreadsheet_csv_config_name, spread_csv_system_id, spread_csv_dnsname, spread_csv_domain, spread_csv_systemstatus, spread_csv_analysisstatus, spread_csv_reason, spread_csv_recommendation, spread_csv_systemtype, spread_csv_ip, spread_csv_os, spread_csv_company, spread_csv_location, spread_csv_serviceprovider, spread_csv_tag, spread_csv_case, spread_csv_system_create_time, spread_csv_system_modify_time) VALUES ('SystemExporterSpreadsheetCsvConfig', TRUE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE, TRUE, FALSE, TRUE, TRUE);"),

            migrations.RunSQL("INSERT INTO dfirtrack_config_systemexporterspreadsheetxlsconfigmodel (system_exporter_spreadsheet_xls_config_name, spread_xls_system_id, spread_xls_dnsname, spread_xls_domain, spread_xls_systemstatus, spread_xls_analysisstatus, spread_xls_reason, spread_xls_recommendation, spread_xls_systemtype, spread_xls_ip, spread_xls_os, spread_xls_company, spread_xls_location, spread_xls_serviceprovider, spread_xls_tag, spread_xls_case, spread_xls_system_create_time, spread_xls_system_modify_time, spread_xls_worksheet_systemstatus, spread_xls_worksheet_analysisstatus, spread_xls_worksheet_reason, spread_xls_worksheet_recommendation, spread_xls_worksheet_tag) VALUES ('SystemExporterSpreadsheetXlsConfig', TRUE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE, TRUE, FALSE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE);"),

            migrations.RunSQL("INSERT INTO dfirtrack_config_SystemImporterFileCsvConfigbasedConfigModel (system_importer_file_csv_configbased_config_name, csv_skip_existing_system, csv_column_system, csv_headline, csv_choice_ip, csv_remove_ip, csv_column_ip, csv_remove_case, csv_remove_company, csv_remove_tag, csv_default_systemstatus_id, csv_default_analysisstatus_id) VALUES ('SystemImporterFileCsvConfigbasedConfig', TRUE, '1', TRUE, FALSE, FALSE, '2', FALSE, FALSE, FALSE, '1', '1');"),

            migrations.RunSQL("INSERT INTO dfirtrack_config_SystemImporterFileCsvFormbasedConfigModel (system_importer_file_csv_formbased_config_name, csv_skip_existing_system, csv_column_system, csv_headline, csv_choice_ip, csv_remove_ip, csv_column_ip, csv_remove_case, csv_remove_company, csv_remove_tag) VALUES ('SystemImporterFileCsvFormbasedConfig', TRUE, '1', TRUE, FALSE, FALSE, '2', FALSE, FALSE, FALSE);"),

        ]

    # SQLite3 (uses 1 / 0 as boolean)
    else:       # coverage: ignore branch

        operations = [

            migrations.RunSQL("INSERT INTO dfirtrack_config_artifactexporterspreadsheetxlsconfigmodel (artifact_exporter_spreadsheet_xls_config_name, artifactlist_xls_artifact_id, artifactlist_xls_system_id, artifactlist_xls_system_name, artifactlist_xls_artifactstatus, artifactlist_xls_artifacttype, artifactlist_xls_artifact_source_path, artifactlist_xls_artifact_storage_path, artifactlist_xls_artifact_note, artifactlist_xls_artifact_md5, artifactlist_xls_artifact_sha1, artifactlist_xls_artifact_sha256, artifactlist_xls_artifact_create_time, artifactlist_xls_artifact_modify_time, artifactlist_xls_worksheet_artifactstatus, artifactlist_xls_worksheet_artifacttype) VALUES ('ArtifactExporterSpreadsheetXlsConfig', 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1);"),

            migrations.RunSQL("INSERT INTO dfirtrack_config_systemexportermarkdownconfigmodel (system_exporter_markdown_config_name, markdown_sorting) VALUES ('SystemExporterMarkdownConfig', 'sys');"),

            migrations.RunSQL("INSERT INTO dfirtrack_config_systemexporterspreadsheetcsvconfigmodel (system_exporter_spreadsheet_csv_config_name, spread_csv_system_id, spread_csv_dnsname, spread_csv_domain, spread_csv_systemstatus, spread_csv_analysisstatus, spread_csv_reason, spread_csv_recommendation, spread_csv_systemtype, spread_csv_ip, spread_csv_os, spread_csv_company, spread_csv_location, spread_csv_serviceprovider, spread_csv_tag, spread_csv_case, spread_csv_system_create_time, spread_csv_system_modify_time) VALUES ('SystemExporterSpreadsheetCsvConfig', 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1);"),

            migrations.RunSQL("INSERT INTO dfirtrack_config_systemexporterspreadsheetxlsconfigmodel (system_exporter_spreadsheet_xls_config_name, spread_xls_system_id, spread_xls_dnsname, spread_xls_domain, spread_xls_systemstatus, spread_xls_analysisstatus, spread_xls_reason, spread_xls_recommendation, spread_xls_systemtype, spread_xls_ip, spread_xls_os, spread_xls_company, spread_xls_location, spread_xls_serviceprovider, spread_xls_tag, spread_xls_case, spread_xls_system_create_time, spread_xls_system_modify_time, spread_xls_worksheet_systemstatus, spread_xls_worksheet_analysisstatus, spread_xls_worksheet_reason, spread_xls_worksheet_recommendation, spread_xls_worksheet_tag) VALUES ('SystemExporterSpreadsheetXlsConfig', 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0);"),

            migrations.RunSQL("INSERT INTO dfirtrack_config_SystemImporterFileCsvConfigbasedConfigModel (system_importer_file_csv_configbased_config_name, csv_skip_existing_system, csv_column_system, csv_headline, csv_choice_ip, csv_remove_ip, csv_column_ip, csv_remove_case, csv_remove_company, csv_remove_tag, csv_default_systemstatus_id, csv_default_analysisstatus_id) VALUES ('SystemImporterFileCsvConfigbasedConfig', 1, '1', 1, 0, 0, '2', 0, 0, 0, '1', '1');"),

            migrations.RunSQL("INSERT INTO dfirtrack_config_SystemImporterFileCsvFormbasedConfigModel (system_importer_file_csv_formbased_config_name, csv_skip_existing_system, csv_column_system, csv_headline, csv_choice_ip, csv_remove_ip, csv_column_ip, csv_remove_case, csv_remove_company, csv_remove_tag) VALUES ('SystemImporterFileCsvFormbasedConfig', 1, '1', 1, 0, 0, '2', 0, 0, 0);"),

        ]
