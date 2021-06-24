
//TODO: Has to go just to keep it running during the transition
// widget configuration
var pstyle = 'border: 1px solid #dfdfdf; padding: 5px;';

var case_data = data_template


var config = {

    ///////////////////
    ///// Layouts /////
    ///////////////////

    main_layout: {
        name: 'main_layout',
        padding: 0,
        panels: [
            { type: 'top', size: 50, style:pstyle,  },
            { type: 'left', size: 200, resizable: true, minSize: 120 },
            { type: 'main', minSize: 550, overflow: 'hidden' }
        ]
    },
    lateral_layout: {
        name: 'lateral_layout',
        padding: 0,
        panels: [
            { type: 'lateral_main', minSize: 550, overflow: 'main' },
            { type: 'lateral_bottom', minSize: 550, overflow: 'bottom' }
        ]
    },

    //////////////////
    ///// Popups /////
    //////////////////

    popup_layout: {
        name: 'popup_layout',
        padding: 0,
        panels: [
            { type: 'main', minSize: 300 }
        ]
    },
    webdav_popup_layout:{

        name: 'webdav_popup_layout',
        padding: 0,
        panels: [
            { type: 'top'},
            { type: 'main', minSize: 300 }
        ]
    },
    about_popup_layout: {
        name: 'about_popup_layout',
        padding: 4,
        panels: [
            { type: 'main', minSize: 200 }
        ]
    },


    /////////////////
    ///// Forms /////
    /////////////////

    case_form: {
        header: 'Edit Case',
        name: 'case_form',
        formURL: './templates/case_details_form.html',
        fields: [
            { name: 'caseid',  type: 'text', html: { caption: 'Case ID', attr: 'size="15"' } },
            { name: 'client', type: 'text', required: true, html: { caption: 'Client', attr:  'maxlength="40"' } },
            { name: 'start_date', type: 'text', required: true,  type: 'date' ,html: { caption: 'Engagement start' }},
            { name: 'summary', type: 'textarea', html: { caption: 'Summary', attr: 'wdith="200px" height="150px" maxlength="600"'  } },
            { name: 'mispserver', type: 'text', required: false },
            { name: 'mispapikey', type: 'text', required: false},
            { name: 'mispeventid', type: 'text', required: false },
            { name: 'vtapikey', type: 'text', required: false },
        ],
        tabs: [
            { id: 'tab_case', caption: 'General' },
            { id: 'tab_misp', caption: 'MISP'},
            { id: 'tab_vt', caption: 'Virustotal'},
        ],
    },
    webdav_form: { //TODO: Refactor using a template
        name: 'webdav_form',
        fields: [
            { name: 'server',  type: 'text', html: { caption: 'Webdav Directory URL', attr: 'size="40"' } },
        ],
        actions: {
            Connect: function () {
                openWebDav()
            }
        }
    },


    ////////////////////
    ///// Toolbars /////
    ////////////////////

    toolbar: {
        name: 'toolbar',
        items: [
            { type: 'menu', id: 'file', text: 'File', icon: 'fa fa-file', items: [
                    { type: 'button', id: 'new_sod', text: 'New Engagement', icon: 'fa fa-plus' },
                    { type: 'button', id: 'open_sod', text: 'Open Engagement (File)', icon: 'fa fa-folder-open' },
                    { type: 'button', id: 'open_webdav', text: 'Open Engagement (WebDav)', icon: 'fa fa-server' },
                    { type: 'button', id: 'save_sod', text: 'Save Engagement', icon: 'fa fa-save' },
                    { type: 'button', id: 'release_lock', text: 'Release Lock for Others', icon: 'fa fa-unlock' },
                    { type: 'button', id: 'request_lock', text: 'Claim Lock to Edit', icon: 'fa fa-lock' },
                    { type: 'button', id: 'force_unlock', text: 'Force Unlock to Edit', icon: 'fa fa-bomb' },
                ]},
            { type: 'button', id: 'case_details', text: 'Case Configuration', icon: 'fa fa-cogs' },
            { type: 'menu', id: 'help', text: 'Help', icon: 'fa fa-question-circle', items: [
                    { type: 'button', id: 'online_help', text: 'Online Help', icon: 'fa fa-globe' },
                    { type: 'button', id: 'about', text: 'About', icon: 'fa fa-info' },
                ]},
            //{ type: 'button', id: 'casenews', text: 'Case News', icon: 'fa fa-newspaper-o' },

            { type: 'spacer' },
            //{ type: 'html',html:"<img onclick=\"browser_open('https://www.infoguard.ch/')\" src='img/ig.png' style='height:30px'>&nbsp;<img onclick=\"browser_open('https://cyberfox.blog/')\" src='img/logo.png'>" },
            { type: 'html',html:"<img onclick=\"browser_open('https://cyberfox.blog/')\" src='img/logo.png'>" },

        ],
    },


    ////////////////////
    ///// Sidebars /////
    ////////////////////

    sidebar: {
        name: 'sidebar',
        bottomHTML : '<div id="lock" style="background-color: #eee; padding: 10px 5px; border-top: 1px solid silver">&#128272; Case unlocked (edits allowed)</div>',
        nodes: [
            { id: 'investigation', text: 'Investigation', group: true, expanded: true, nodes: [
                    { id: 'timeline', text: 'Timeline', icon: 'fa fa-clock-o'},
                    { id: 'investigated_systems', text: 'Investigated Systems', icon: 'fa fa-search-plus' },
                    { id: 'malware', text: 'Malware/Tools', icon: 'fa fa-bug'},
                    { id: 'accounts', text: 'Compromised Accounts', icon: 'fa fa-users'},
                    { id: 'network', text: 'Network Indicators', icon: 'fa fa-sitemap'},
                    { id: 'exfiltration', text: 'Exfiltration', icon: 'fa fa-tint'},
                    { id: 'osint', text: 'OSInt', icon: 'fa fa-globe'},
                    { id: 'systems', text: 'Systems', icon: 'fa fa-desktop'},
                ]},
            { id: 'reporting', text: 'Reporting', group: true, expanded: true, nodes: [
                    { id: 'vis_timeline', text: 'Visual Timeline', icon: 'fa fa-calendar-o'},
                    { id: 'lateral', text: 'Lateral Movement', icon: 'fa fa-share-alt'},
                    { id: 'activity', text: 'Activity Plot', icon: 'fa fa-bar-chart'}
                ]},
            { id: 'case_management', text: 'Case Management', group: true, expanded: true, nodes: [
                    { id: 'investigators', text: 'Investigators', icon: 'fa fa-user'},
                    { id: 'evidence', text: 'Evidence', icon: 'fa fa-gavel'},
                    { id: 'actions', text: 'Action Items', icon: 'fa fa-briefcase'},
                    { id: 'casenotes', text: 'Case Notes', icon: 'fa fa-sticky-note'},
                ]
            },

        ],
    },

    /////////////////////////
    ///// Timeline GRID /////
    /////////////////////////

    grd_timeline: {
        name: 'grd_timeline',
        show: {
            toolbar: true,
            footer: true
        },
        menu: [

            { id: "duplicate", text: 'Duplicate Line', icon: 'fa fa-copy'},
        ],
        multiSearch: true,
        searches: [
            { field: 'event_data', caption: 'Event', type: 'text' },
            { field: 'event_type', caption: 'Event Type', type: 'list', options:{items:case_data.event_types} },
            { field: 'event_host', caption: 'Event System', type: 'text' },
            { field: 'event_source_host', caption: 'Source System', type: 'text'},
            { field: 'killchain', caption: 'Killchain', type: 'list', options:{items:case_data.killchain}},
            { field: 'notes', caption: 'Notes', type: 'text' },
            { field: 'attribution', caption: 'Attribution', type: 'text' }
        ],
        columns: [
            { field: 'date_time', caption: 'Date/Time', type:"text",size: '140px',editable: { type: 'datetime' } ,sortable: true },
            { field: 'event_type', sortable: true,caption: 'Type', size: '80px',
                editable: { type: 'list', items: case_data.event_types, showAll: true },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }},
            { field: 'event_host',sortable: true, caption: 'Event System', size: '120px', editable: { type: 'list', items: case_data.systems, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }},
            { field: 'direction',sortable: true, caption: '⇄', size: '40px', editable: { type: 'list', items: case_data.direction, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }},
            { field: 'event_source_host',sortable: true, caption: 'Remote System', size: '120px', editable: { type: 'list', items: case_data.systems, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }},
            { field: 'killchain',sortable: true, caption: 'Killchain', size: '100px',
                editable: { type: 'list', items: case_data.killchain, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }},
            { field: 'event_data', caption: 'Event', size: '100%', info: true, editable: { type: 'text', min: 10, max: 500 }},
            { field: 'notes', caption: 'Notes', size: '200px', editable: { type: 'text', min: 0, max: 200 }},
            { field: 'visual',sortable: true, caption: 'Visual?', size: '40px', type:"checkbox", editable: { type: 'checkbox' }},
            { field: 'followup',sortable: true, caption: 'Followup', size: '40px', type:"checkbox", editable: { type: 'checkbox' }},
            { field: 'attribution', sortable: true,caption: 'Attribution', size: '80px' , editable: { type: 'text', min: 0, max: 20 }},
            { field: 'owner',sortable: true, caption: 'Owner', size: '100px',
                editable: { type: 'list', items: case_data.investigators, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }}
        ],
        toolbar: {
            items: [
                { id: 'add', type: 'button', caption: 'Add Item', icon: 'w2ui-icon-plus' },
                { id: 'remove', type: 'button', caption: 'Remove Item', icon: 'fa fa-minus' },
                { id: 'import', type: 'button', caption: 'Import CSV', icon: 'fa fa-upload' },
                { id: 'export', type: 'button', caption: 'Export CSV', icon: 'fa fa-download' }
            ],
        },
        records: [
        ],
    },


    //////////////////////////////////////
    ///// Investigated Systems  GRID /////
    //////////////////////////////////////

    grd_investigated_systems: {
        name: 'grd_investigated_systems',
        show: {
            toolbar: true,
            footer: true
        },
        menu: [

            { id: "to_tl", text: 'To Timeline', icon: 'fa fa-clock-o' },
            { id: "duplicate", text: 'Duplicate Line', icon: 'fa fa-copy'}
        ],
        multiSearch: true,
        searches: [
            { field: 'summary', caption: 'Summary', type: 'text' },
            { field: 'hostname', caption: 'Hostname', type: 'text' },
            { field: 'analysis_status', caption: 'Analysis Status', type: 'list', options:{items:case_data.status} },
            { field: 'analyst', caption: 'Analyst', type: 'text'},
            { field: 'verdict', caption: 'Verdict', type: 'list', options:{items:case_data.verdicts} },
            { field: 'report_status', caption: 'Report Status', type: 'list', options:{items:case_data.status} }
        ],
        columns: [
            { field: 'date_added', sortable: true,caption: 'Date added', size: '80px' , render:'date:YYYY-MM-DD' },
            { field: 'date_updated', sortable: true,caption: 'Date updated', size: '80px',render:'date:YYYY-MM-DD'  },
            { field: 'first_compromise', sortable: true,caption: 'First Compromise', size: '140px', editable: { type: 'datetime' }},
            { field: 'hostname', caption: 'Hostname', size: '140px' ,editable: { type: 'list', items: case_data.systems, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }},
            { field: 'verdict',sortable: true, caption: 'Verdict', size: '70px' ,
                editable: { type: 'list', items: case_data.verdicts, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }},
            { field: 'summary', caption: 'Summary', size: '100%',info: true, editable: { type: 'text', min: 0, max: 500 }},
            { field: 'analysis_required',sortable: true, caption: 'Analysis req?', size: '40px', editable: { type: 'checkbox'} },
            { field: 'analysis_status', sortable: true,caption: 'Analysis status', size: '80px',
                editable: { type: 'list', items: case_data.status, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }},
            { field: 'analyst', sortable: true,caption: 'Analyst', size: '80px',
                editable: { type: 'list', items: case_data.investigators, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }},
            { field: 'report_status', sortable: true,caption: 'Report Status', size: '40px',editable: { type: 'list', items: case_data.status, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                } }
        ],
        toolbar: {
            items: [
                { id: 'add', type: 'button', caption: 'Add Record', icon: 'w2ui-icon-plus' },
                { id: 'remove', type: 'button', caption: 'Remove Item', icon: 'fa fa-minus' },
                { id: 'import', type: 'button', caption: 'Import CSV', icon: 'fa fa-upload' },
                { id: 'export', type: 'button', caption: 'Export CSV', icon: 'fa fa-download' }
            ],
        },
        records: [

        ],
    },


    /////////////////////////
    ///// Malware  GRID /////
    /////////////////////////

    grd_malware: {
        name: 'grd_malware',
        show: {
            toolbar: true,
            footer: true
        },
        menu: [
            { id: "duplicate", text: 'Duplicate Line', icon: 'fa fa-copy'},
            { id: "to_hosts", text: 'To hosts', icon: 'fa fa-bullseye' },
            { id: "to_tl", text: 'To Timeline', icon: 'fa fa-clock-o' },
            { id: 'misp', type: 'button', caption: 'Send to MISP', icon: 'fa fa-cloud' },
            { id: 'vt', type: 'button', caption: 'Check VT', icon: 'fa fa-search' },
        ],
        multiSearch: true,
        searches: [
            { field: 'text', caption: 'Filename', type: 'text' },
            { field: 'path_on_disk',  caption: 'Path', type: 'text' },
            { field: 'hostname', caption: 'System', type: 'text' },
            { field: 'md5', caption: 'Hash', type: 'text'},
            { field: 'notes', caption: 'Notes', type: 'text' },
            { field: 'attribution',  caption: 'Attribution', type: 'text' },
        ],
        columns: [
            { field: 'date_added', sortable: true,caption: 'Date added', render:'date:YYYY-MM-DD' , type:'date', size: '80px'},
            { field: 'text', sortable: true,caption: 'Filename', size: '150px', editable: { type: 'text', min: 1, max: 100 }},
            { field: 'path_on_disk', sortable: true,caption: 'Path on Disk', size: '200px', editable: { type: 'text', min: 1, max: 150 } },
            { field: 'creation_date', sortable: true, caption: 'Creation Date',  size: '120px', editable: { type: 'datetime' } },
            { field: 'modification_date', sortable: true, caption: 'Last modified',  size: '120px', editable: { type: 'datetime' } },
            { field: 'hostname', sortable: true,caption: 'Host', size: '140px', editable: { type: 'list', items: case_data.systems, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }},
            { field: 'md5', sortable: true,caption: 'Hash', size: '60px' , editable: { type: 'text', min: 32, max: 128 }},
            { field: 'vt', sortable: true,caption: 'vt', size: '20px',
                render: function(record){
                    icon = "unknown.png"
                    caption = "Not checked"

                    if(record.vt == "infected") {
                        icon="virus.png"
                        caption = "Malicious"
                    }
                    if(record.vt == "clean") {
                        icon="clean.png"
                        caption = "Clean"
                    }
                    if(record.vt == "noresult") {
                        icon="no_results.png"
                        caption = "No results on VT"
                    }
                    html = '<img src="./img/'+icon+'" alt="'+caption+'" style="width:16px;height:16px" >'
                    return html
                }
            },
            { field: 'attribution',sortable: true, caption: 'Attribution', size: '80px' , editable: { type: 'text', min: 0, max: 20 }},
            { field: 'notes', sortable: true,caption: 'notes', size: '100%', editable: { type: 'text', min: 0, max: 500 },info: true},

        ],
        toolbar: {
            items: [
                { id: 'add', type: 'button', caption: 'Add Malware', icon: 'w2ui-icon-plus' },
                { id: 'remove', type: 'button', caption: 'Remove Item', icon: 'fa fa-minus' },
                { id: 'import', type: 'button', caption: 'Import CSV', icon: 'fa fa-upload' },
                { id: 'export', type: 'button', caption: 'Export CSV', icon: 'fa fa-download' }
            ],
        },
        records: [

        ],
    },


    /////////////////////////////////////
    ///// Compromised Accounts GRID /////
    /////////////////////////////////////

    grd_accounts: {
        name: 'grd_accounts',
        show: {
            toolbar: true,
            footer: true
        },
        menu: [

            { id: "duplicate", text: 'Duplicate Line', icon: 'fa fa-copy'},
        ],
        multiSearch: true,
        searches: [
            { field: 'account_name', caption: 'Account Name', type: 'text' },
            { field: 'domain', caption: 'Domain', type: 'text' },
            { field: 'sid', caption: 'SID', type: 'text' },
            { field: 'context', caption: 'Context', type: 'text' },
            { field: 'privileges', caption: 'Privileges', type: 'text' },
            { field: 'attribution', caption: 'Attribution', type: 'text' },
        ],
        columns: [
            { field: 'date_added', sortable: true,caption: 'Date added', render:'date:YYYY-MM-DD' , type:'date', size: '80px',sortable: true },
            { field: 'account_name', sortable: true,caption: 'Account Name', size: '120px', editable: { type: 'text', min: 0, max: 100 } },
            { field: 'domain', sortable: true,caption: 'Account Domain', size: '120px' , editable: { type: 'text', min: 0, max: 80 }},
            { field: 'sid', sortable: true,caption: 'SID', size: '200px',  editable: { type: 'text', min: 0, max: 80 }},
            { field: 'context', sortable: true,caption: 'Context', size: '100%', info: true, editable: { type: 'text', min: 0, max: 500 }},
            { field: 'last_activity', sortable: true,caption: 'Last Activity', type:"datetime",size: '140px',editable: { type: 'datetime' } },
            { field: 'privileges', sortable: true,caption: 'Privileges', size: '120px', type:"text", editable: { type: 'text' }},
            { field: 'attribution',sortable: true, caption: 'Attribution', size: '80px' , editable: { type: 'text', min: 0, max: 20 }},
        ],
        toolbar: {
            items: [
                { id: 'add', type: 'button', caption: 'Add Item', icon: 'w2ui-icon-plus' },
                { id: 'remove', type: 'button', caption: 'Remove Item', icon: 'fa fa-minus' },
                { id: 'import', type: 'button', caption: 'Import CSV', icon: 'fa fa-upload' },
                { id: 'export', type: 'button', caption: 'Export CSV', icon: 'fa fa-download' }
            ],
        },
        records: [],
    },


    ////////////////////////
    ///// Network GRID /////
    ////////////////////////

    grd_network: {
        name: 'grd_network',
        show: {
            toolbar: true,
            footer: true
        },
        menu: [
            { id: "duplicate", text: 'Duplicate Line', icon: 'fa fa-copy'},
            { id: 'misp', type: 'button', caption: 'Send to MISP', icon: 'fa fa-cloud' },
        ],
        multiSearch: true,
        searches: [
            { field: 'ip', caption: 'IP', type: 'text' },
            { field: 'domainname', caption: 'Domainname', type: 'text' },
            { field: 'port', caption: 'Port', type: 'int' },
            { field: 'context', caption: 'Context', type: 'text' },
            { field: 'malware', caption: 'Malware', type: 'text' },
            { field: 'whois', caption: 'Whois', type: 'text' },
            { field: 'attribution', caption: 'Attribution', type: 'text' },
        ],
        columns: [
            { field: 'date_added', sortable: true,caption: 'Date added', render:'date:YYYY-MM-DD' , type:'date', size: '80px'},
            { field: 'ip', sortable: true,caption: 'IP', size: '120px', editable: { type: 'text', min: 7, max: 15 } },
            { field: 'domainname',sortable: true, caption: 'Domainname', size: '120px' , editable: { type: 'text', min: 0, max: 180 }},
            { field: 'port', sortable: true,caption: 'Port', size: '40px', type:"number", editable: { type: 'number' }},
            { field: 'context', caption: 'Context', size: '100%', info: true, editable: { type: 'text', min: 0, max: 500 }},
            { field: 'last_activity',sortable: true, caption: 'Last activity' , type:'datetime', size: '80px', editable: { type: 'datetime'} },
            { field: 'malware', sortable: true,caption: 'Malware', size: '120px', type:"text", editable: { type: 'list', items: case_data.malware, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }},
            { field: 'whois', caption: 'Whois', size: '100px', editable: { type: 'text', min: 0, max: 1500 }},
            { field: 'attribution', sortable: true,caption: 'Attribution', size: '80px' , editable: { type: 'text', min: 0, max: 20 }},

        ],
        toolbar: {
            items: [
                { id: 'add', type: 'button', caption: 'Add Item', icon: 'w2ui-icon-plus' },
                { id: 'remove', type: 'button', caption: 'Remove Item', icon: 'fa fa-minus' },
                { id: 'import', type: 'button', caption: 'Import CSV', icon: 'fa fa-upload' },
                { id: 'export', type: 'button', caption: 'Export CSV', icon: 'fa fa-download' }
            ],
        },
        records: [],
    },

    /////////////////////////////
    ///// Exfiltration GRID /////
    /////////////////////////////

    grd_exfiltration: {
        name: 'grd_exfiltration',
        show: {
            toolbar: true,
            footer: true
        },
        menu: [
            { id: "duplicate", text: 'Duplicate Line', icon: 'fa fa-copy'},
            { id: "to_tl", text: 'To Timeline', icon: 'fa fa-clock-o' },
        ],
        multiSearch: true,
        searches: [
            { field: 'stagingsystem', caption: 'Staging System', type: 'text' },
            { field: 'original', caption: 'Original System', type: 'text' },
            { field: 'filename', caption: 'Filename', type: 'text' },
            { field: 'size', caption: 'Size', type: 'int' },
            { field: 'contents', caption: 'Contents', type: 'text' },
            { field: 'notes', caption: 'Notes', size: '100%',type: 'text' },
            { field: 'attribution', caption: 'Attribution', type: 'text' },
        ],
        columns: [
            { field: 'created', sortable: true,caption: 'Created' , type:'datetime', size: '100px', editable: { type: 'datetime'} },
            { field: 'exfiltime', sortable: true,caption: 'Exfil Time' , type:'datetime', size: '100px', editable: { type: 'datetime'} },
            { field: 'stagingsystem', sortable: true,caption: 'Staging System', size: '120px', editable: { type: 'list', items: case_data.systems, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                } },
            { field: 'original',sortable: true, caption: 'Original System', size: '120px', editable: { type: 'list', items: case_data.systems, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                } },
            { field: 'exfil_to',sortable: true, caption: 'Exfiltrated to', size: '120px', editable: { type: 'list', items: case_data.systems, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                } },
            { field: 'filename',sortable: true, caption: 'Filename', size: '120px' , editable: { type: 'text', min: 0, max: 180 }},
            { field: 'size',sortable: true, caption: 'Size', size: '100px', type:"number", editable: { type: 'number' }},
            { field: 'contents', caption: 'Contents', size: '100%', info: true, editable: { type: 'text', min: 0, max: 1500 }},
            { field: 'notes', caption: 'Context', size: '180px', editable: { type: 'text', min: 0, max: 1500 }},
            { field: 'attribution', sortable: true,caption: 'Attribution', size: '80px' , editable: { type: 'text', min: 0, max: 20 }},

        ],
        toolbar: {
            items: [
                { id: 'add', type: 'button', caption: 'Add Item', icon: 'w2ui-icon-plus' },
                { id: 'remove', type: 'button', caption: 'Remove Item', icon: 'fa fa-minus' },
                { id: 'import', type: 'button', caption: 'Import CSV', icon: 'fa fa-upload' },
                { id: 'export', type: 'button', caption: 'Export CSV', icon: 'fa fa-download' }
            ],
        },
        records: []
    },


    ///////////////////////
    ///// OSINT  GRID /////
    ///////////////////////

    grd_osint: {
        name: 'grd_osint',
        show: {
            toolbar: true,
            footer: true
        },
        columns: [

            { field: 'text', sortable: true, caption: 'Short Name', size: '100px', editable: { type: 'text' }  },
            { field: 'url',sortable: true, caption: 'URL', size: '200px',editable: { type: 'text' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return "<a href=\"javascript:browser_open('"+html+"')\">"+html+"</a>" || '';
                }
            },
            { field: 'desc', sortable: true,caption: 'Description' ,size:"100%", editable: { type: 'text'  } },

        ],
        toolbar: {
            items: [
                { id: 'add', type: 'button', caption: 'Add OSInt', icon: 'w2ui-icon-plus' },
                { id: 'remove', type: 'button', caption: 'Remove OSInt', icon: 'fa fa-minus' },
                { id: 'import', type: 'button', caption: 'Import CSV', icon: 'fa fa-upload' },
                { id: 'export', type: 'button', caption: 'Export CSV', icon: 'fa fa-download' }
            ],
        },
        records: []
    },


    ////////////////////////
    ///// Systems GRID /////
    ////////////////////////

    grd_systems: {
        name: 'grd_systems',
        show: {
            toolbar: true,
            footer: true,
            selectColumn: true
        },
        multiSearch: true,
        searches: [
            { field: 'ip', caption: 'IP', type: 'text' },
            { field: 'text', caption: 'Hostname', type: 'text' },
            { field: 'os', caption: 'Operating System', type: 'text' },
            { field: 'system_type', caption: 'System Type', type: 'list', options:{items:case_data.system_types} },
            { field: 'owner', caption: 'Owner', type: 'text' },
            { field: 'description', caption: 'Description', type: 'text' },
        ],
        columns: [
            { field: 'text',sortable: true, caption: 'Hostname', size: '250px', editable: { type: 'text', min: 1, max: 100 } },
            { field: 'ip',sortable: true, caption: 'IP', size: '110px', editable: { type: 'text', min: 7, max: 15 } },
            { field: 'system_type', sortable: true, caption: 'Type', size: '120px',
                editable: { type: 'list', items: case_data.system_types, showAll: true },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }
            },
            { field: 'os',sortable: true, caption: 'Operating System', size: '250px', editable: { type: 'text', min: 0, max: 30 } },
            { field: 'owner',sortable: true, caption: 'Owner', size: '100px', editable: { type: 'text'} },
            { field: 'description',sortable: true, caption: 'Description', size: '100%', editable: { type: 'text' } },
            { field: 'pin',sortable: true, caption: 'Pin', size: '20px', editable: { type: 'checkbox' } },
        ],
        toolbar: {
            items: [
                { id: 'add', type: 'button', caption: 'Add Item', icon: 'w2ui-icon-plus' },
                { id: 'remove', type: 'button', caption: 'Remove Item', icon: 'fa fa-minus' },
                { id: 'import', type: 'button', caption: 'Import CSV', icon: 'fa fa-upload' },
                { id: 'export', type: 'button', caption: 'Export CSV', icon: 'fa fa-download' },
                { id: 'import', type: 'button', caption: 'Import CSV', icon: 'fa fa-upload' },
                { id: 'export', type: 'button', caption: 'Export CSV', icon: 'fa fa-download' }
            ],
        },
        records: []
    },


    ///////////////////////////////
    ///// Investigators  GRID /////
    ///////////////////////////////

    grd_investigators: {
        name: 'grd_investigators',
        show: {
            toolbar: true,
            footer: true
        },
        multiSearch: true,
        searches: [
            { field: 'text', caption: 'Short Name', type: 'text' },
            { field: 'full_name', caption: 'Full Name', type: 'text'},
            { field: 'affiliation', caption: '🏢 Affiliation', type: 'text' },
            { field: 'role', caption: '🙋 Role', type: 'text'},
            { field: 'contact_email', caption: '📬 Email', type: 'text'},
            { field: 'contact_phone', caption: '📱 Phone', type: 'text'},
            { field: 'contact_other', caption: '📖 Other', type: 'text' }
        ],
        columns: [
            { field: 'text', sortable: true, caption: 'Short Name', size: '100px', editable: { type: 'text', min: 3, max: 5 } },
            { field: 'full_name', sortable: true, caption: 'Full Name', size: '100%', editable: { type: 'text', min: 5, max: 40 } },
            { field: 'affiliation', sortable: true, caption: '🏢 Affiliation', size: '100px',editable: { type: 'text', min: 5, max: 40 } },
            { field: 'role', sortable: true, caption: '🙋 Role', size: '150px', editable: { type: 'text', min: 0, max: 40 } },
            { field: 'contact_email', sortable: true, caption: '📬 Email', size: '150px', editable: { type: 'text', min: 5, max: 40 } },
            { field: 'contact_phone', sortable: true, caption: '📱 Phone', size: '100px', editable: { type: 'text', min: 5, max: 40 } },
            { field: 'contact_other', sortable: true, caption: '📖 Other', size: '250px', editable: { type: 'text', min: 5, max: 40 } },
        ],
        toolbar: {
            items: [
                { id: 'add', type: 'button', caption: 'Add Investigator', icon: 'w2ui-icon-plus' },
                { id: 'remove', type: 'button', caption: 'Remove Investigator', icon: 'fa fa-minus' },
                { id: 'import', type: 'button', caption: 'Import CSV', icon: 'fa fa-upload' },
                { id: 'export', type: 'button', caption: 'Export CSV', icon: 'fa fa-download' }
            ],
        },
        records: []
    },

    //////////////////////////
    ///// Evidence  GRID /////
    //////////////////////////

    grd_evidence: {
        name: 'grd_evidence',
        show: {
            toolbar: true,
            footer: true
        },
        menu: [
            { id: "duplicate", text: 'Duplicate Line', icon: 'fa fa-copy'},
        ],
        multiSearch: true,
        searches: [
            { field: 'type', caption: 'Type', type: 'list', options: {items: case_data.evidence_types} },
            { field: 'name', caption: 'Name', type: 'text' },
            { field: 'description', caption: 'Description', type: 'text' },
            { field: 'provider', caption: 'Provider', type: 'text' },
            { field: 'hash', caption: 'Hash', type: 'text' },
            { field: 'location', caption: 'Location', type: 'text' },
        ],
        columns: [
            { field: 'date_acquired', sortable: true,caption: 'Date Acquired', editable: { type: 'datetime' } , type:'date', size: '130px',sortable: true },
            { field: 'type',sortable: true, caption: 'Type', size: '125px', editable: { type: 'list', items: case_data.evidence_types, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }
            },
            { field: 'name',sortable: true, caption: 'Name', size: '130px', editable: { type: 'text'}  },
            { field: 'description',sortable: true, caption: 'Description', size: '100%',editable: { type: 'text' }  },
            { field: 'size', sortable: true,caption: 'Size', size: '60px' , editable: { type: 'text' }},
            { field: 'hash', sortable: true,caption: 'Hash', size: '150px' , editable: { type: 'text' }},
            { field: 'provider', caption: 'Provided by', size: '200px', editable: { type: 'list', items: case_data.investigators, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }
            },
            { field: 'location', sortable: true,caption: 'Location', size: '150px' , editable: { type: 'text' }},
        ],
        toolbar: {
            items: [
                { id: 'add', type: 'button', caption: 'Add Evidence', icon: 'w2ui-icon-plus' },
                { id: 'remove', type: 'button', caption: 'Remove Evidence', icon: 'fa fa-minus' },
                { id: 'import', type: 'button', caption: 'Import CSV', icon: 'fa fa-upload' },
                { id: 'export', type: 'button', caption: 'Export CSV', icon: 'fa fa-download' }
            ],
        },
        records: []
    },


    ////////////////////////
    ///// Actions GRID /////
    ////////////////////////

    grd_actions: {
        name: 'grd_actions',
        show: {
            toolbar: true,
            footer: true
        },
        multiSearch: true,
        searches: [
            { field: 'task', caption: 'Task', type: 'text' },
            { field: 'status', caption: 'Status', type: 'text' },
            { field: 'task_type', caption: 'Type', type: 'list', options:{items:case_data.task_types} },
            { field: 'owner', caption: 'Owner', type: 'text' },
        ],
        columns: [
            { field: 'date_added',sortable: true, caption: 'Date added', render:'date:YYYY-MM-DD' , type:'date', size: '80px'},
            { field: 'date_due',sortable: true, caption: 'Date Due', render:'date:YYYY-MM-DD' , type:'date', size: '80px', editable: { type: 'date'} },
            { field: 'task_type',sortable: true, caption: 'Type', size: '150px', editable: { type: 'list', items: case_data.task_types, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }},
            { field: 'task', sortable: true,caption: 'Task', size: '100%', info:true, editable: { type: 'text', min: 1, max: 1500 } },
            { field: 'status',sortable: true, caption: 'Status', size: '250px', editable: { type: 'list', items: case_data.status, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }},
            { field: 'owner', caption: 'Owner', size: '250px', editable: { type: 'list', items: case_data.investigators, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }},
        ],
        toolbar: {
            items: [
                { id: 'add', type: 'button', caption: 'Add Item', icon: 'w2ui-icon-plus' },
                { id: 'remove', type: 'button', caption: 'Remove Item', icon: 'fa fa-minus' },
                { id: 'import', type: 'button', caption: 'Import CSV', icon: 'fa fa-upload' },
                { id: 'export', type: 'button', caption: 'Export CSV', icon: 'fa fa-download' }
            ],
        },
        records: []
    },


    ///////////////////////////
    ///// Case Notes GRID /////
    ///////////////////////////

    grd_casenotes: {
        name: 'grd_casenotes',
        show: {
            toolbar: true,
            footer: true
        },
        columns: [
            { field: 'date_added',sortable: true, caption: 'Date added', render:'date:YYYY-MM-DD' , type:'date', size: '80px'},
            { field: 'note', sortable: true,caption: 'Note', size: '100%', info:true, editable: { type: 'text', min: 1, max: 1500 } },
            { field: 'owner', caption: 'Owner', size: '250px', editable: { type: 'list', items: case_data.investigators, showAll: true ,  match: 'contains' },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }},
        ],
        toolbar: {
            items: [
                { id: 'add', type: 'button', caption: 'Add Item', icon: 'w2ui-icon-plus' },
                { id: 'remove', type: 'button', caption: 'Remove Item', icon: 'fa fa-minus' },
                { id: 'import', type: 'button', caption: 'Import CSV', icon: 'fa fa-upload' },
                { id: 'export', type: 'button', caption: 'Export CSV', icon: 'fa fa-download' }
            ],
        },
        records: []
    },


    ////////////////////////////
    ///// Add to MISP GRID /////
    ////////////////////////////
    grd_add_misp: {
        name: 'grd_add_misp',
        show: {
            toolbar: true,
            footer: false,
            selectColumn: true,
            toolbarSearch: false
        },
        columns: [
            { field: 'aurora_field_type', sortable: true,caption: 'Field Type', size: '90px' },
            { field: 'misp_field_type', sortable: true,caption: "MISP Type", size: '90px', info:true, editable: { type: 'list', items: misp_attribute_types, showAll: true },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                } },
            { field: 'value', sortable: true,caption: 'Value', size: '100px', info:true},
            { field: 'comment', sortable: true,caption: 'Comment', size: '100%', info:true,editable: { type: 'text', min: 1, max: 1500 }},
        ],
        toolbar: {
            items: [
                { id: 'send', type: 'button', caption: 'Send', icon: 'fa fa-cloud' },
            ],
        },
        records: []
    },



    ////////////////////////////
    ///// Import Mapping /////
    ////////////////////////////
    grd_import_mapping: {
        name: 'grd_import_mapping',
        show: {
            toolbar: true,
            footer: false,
            selectColumn: false,
            toolbarSearch: false
        },
        columns: [
            { field: 'grid', sortable: true,caption: 'Grid Field', size: '50%'},
            { field: 'csv', sortable: true,caption: 'First line of CSV', size: '50%', editable: { type: 'list', items: [], showAll: true },
                render: function (record, index, col_index) {
                    var html = this.getCellValue(index, col_index);
                    return html || '';
                }},
        ],
        toolbar: {
            items: [
                { id: 'import', type: 'button', caption: 'Import', icon: 'fa fa-upload' },
            ],
        },
        records: []
    },
};










/**
 * Content for about popup
 */
about_content = `

    <div id="aboutcontent" style="position: absolute; left: 5px; top: 5px; right: 5px; bottom: 5px;">
    <p>Aurora 0.6.6</p>
    (c) 2018-2021 Mathias Fuchs (<a onclick="browser_open('https://cyberfox.blog')" href="#">https://cyberfox.blog</a>)
    <p>Released under Apache 2.0 License</p>
    <p>Supported and used by <a onclick="browser_open('https://www.infoguard.ch')" href="#">InfoGuard</a></p>
    <p>Application build using electron.js - <a onclick="browser_open('https://electronjs.org')"  href="#">https://electronjs.org</a></p>
    <p>Icons provided by <a onclick="browser_open('https://icons8.com')"  href="#">https://icons8.com</a> and <a onclick="browser_open('https://fontawesome.com')"  href="#">https://fontawesome.com</a> </p>
    <p>UI designed using <a onclick="browser_open('http://w2ui.com')"  href="#">http://w2ui.com</a></p>
    <p>Visualization uses <a onclick="browser_open('http://visjs.org')"  href="#">http://visjs.org</a> and <a onclick="browser_open('https://www.chartjs.org')"  href="#">https://www.chartjs.org</a></p>

     <p>
        <img src="img/logo.png">
        <img src="img/ig.png">
    </p>

    </div>
    `
