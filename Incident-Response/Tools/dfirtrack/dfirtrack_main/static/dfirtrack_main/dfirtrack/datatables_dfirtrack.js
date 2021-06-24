$(document).ready( function () {
    $('#table_analystmemo').DataTable( {
        "pageLength": 15,
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
        "order": [[ 5, "desc" ]]
    } );
    $('#table_entry').DataTable( {
        "pageLength": 30,
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
        "order": [[ 3, "asc" ]]
    } );
    $('#table_reportitem').DataTable( {
        "pageLength": 15,
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
        "order": [[ 5, "desc" ]]
    } );
    $('#table_system').DataTable( {
        "pageLength": 25,
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
        "order": [[ 1, "asc" ]],
        "processing":true,
        "serverSide":true,
        "ajax": {
            "type" : "GET",
            "url": window.location.protocol+"//"+window.location.hostname+(window.location.port ? ':'+location.port: '')+"/system/json/"
        },
        "columns": [
            { "data": "system_id" },
            { "data": "system_name" },
            { "data": "systemstatus" },
            { "data": "analysisstatus" },
            { "data": "system_create_time" },
            { "data": "system_modify_time" }
        ]
    } );
    $('#table_system_task_done').DataTable( {
        "pageLength": 10,
        "order": [[ 0, "asc" ]],
        "columnDefs": [
            { "width": "3%", "targets": 0 },
            { "width": "17%", "targets": 1 },
            { "width": "10%", "targets": 2 },
            { "width": "10%", "targets": 3 },
            { "width": "10%", "targets": 4 },
            { "width": "20%", "targets": 5 },
            { "width": "10%", "targets": 6 },
            { "width": "10%", "targets": 7 },
        ]
    } );
    $('#table_system_task_open').DataTable( {
        "pageLength": 10,
        "order": [[ 0, "asc" ]],
        "columnDefs": [
            { "width": "3%", "targets": 0 },
            { "width": "17%", "targets": 1 },
            { "width": "10%", "targets": 2 },
            { "width": "5%", "targets": 3 },
            { "width": "5%", "targets": 4 },
            { "width": "10%", "targets": 5 },
            { "width": "5%", "targets": 6 },
            { "width": "15%", "targets": 7 },
            { "width": "10%", "targets": 8 },
            { "width": "10%", "targets": 9 },
        ]
    } );
    $('#table_systemhistory').DataTable( {
        "pageLength": 10,
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
        "order": [[ 2, "des" ]]
    } );
    $('#table_task').DataTable( {
        "pageLength": 15,
        "lengthMenu": [[15, 25, 50, -1], [15, 25, 50, "All"]],
        "order": [[ 2, "asc" ]]
    } );
    $('#table_timeline').DataTable( {
        "pageLength": 30,
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
        "order": [[ 1, "asc" ]]
    } );
} );
