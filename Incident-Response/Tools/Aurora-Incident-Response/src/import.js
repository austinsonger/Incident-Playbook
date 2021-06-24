
import_lines = []
import_fieldset = []
import_grid = null
firstline = []  //needed for import mapping


function show_import_dialog(grid){

    // open file
    const {remote} = require('electron')
    const {dialog} = remote
    const path = dialog.showOpenDialog({filters:[{name:"CSV File"}]});

    if(path == undefined) return;

    var fs = require('fs');

    w2utils.lock($( "#main" ),"Loading File...",true)

    var filebuffer = fs.readFileSync(path.toString());

    fieldset = []
    import_fieldset = []
    import_grid = grid

    for(var i=0;i<grid.columns.length;i++){
        if(grid.columns[i].caption=="Date added") continue; // don't show date added
        fieldset.push(grid.columns[i].caption)
        import_fieldset.push(grid.columns[i].field)
    }

    filebuffer= filebuffer.toString()
    import_lines = filebuffer.split(/(?:\r\n|\n)+/)
    w2utils.unlock($( "#main" ))
    openImportPopup(fieldset,import_lines,import_fieldset)

}

function import_data() {
    if (import_lines.length < 1) {
        alert("Could not import. Empty file.")
        w2popup.close()
        return
    }
    w2ui.grd_import_mapping.save()
    w2utils.lock($( "#main" ),"Parsing data...",true)

    mappings=[]
    for(var i = 0; i<w2ui.grd_import_mapping.records.length;i++){

        rcd = w2ui.grd_import_mapping.records[i]
        if(rcd.csv == "") continue
        mapping = {field:rcd.fieldname,column:firstline.indexOf(rcd.csv)}
        mappings.push(mapping)
    }

    //when adding only add existing fields. so iun the add loop rather than going through the input data go through the mapping data and add only what's in there

    //build import data
    for(var i=0;i<import_lines.length;i++){
        fields = CSVtoArrayEasy(import_lines[i])
       // console.log(fields)
        var import_object = {}
        if(!fields) continue
        import_object["recid"]=getNextRECID(import_grid)
        import_object["date_added"] = (new Date()).getTime()

        for(var j =0; j<mappings.length;j++){
            import_object[mappings[j].field]=fields[mappings[j].column]
        }
        //console.log("=== Import Object "+i+ " ===")
        //console.log(import_object)
        import_grid.add(import_object)

    }


    import_grid.refresh()
    w2utils.unlock($( "#main" ))
    w2popup.close()
}