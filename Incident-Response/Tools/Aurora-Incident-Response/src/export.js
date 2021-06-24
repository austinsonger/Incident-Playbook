function export_csv(grid){

    const {remote} = require('electron')
    const {dialog} = remote
    const selectedPath = dialog.showSaveDialog({filters: [{name: "Export File", extensions: ["csv"]}]});
    if (selectedPath == undefined) {

        w2alert('No file selected. Could not export.');
        return false

    }
    csv =""
    //generate header line
    headerline = ""
    for(var i=0; i<grid.columns.length;i++) {
        headerline += grid.columns[i].caption
        if(i<grid.columns.length-1) headerline += ","
    }

    csv += headerline + "\n"

    //generate content
    for(var i = 0;i < grid.records.length;i++){

       line = ""
       for(var j=0; j<grid.columns.length;j++) {
           data = grid.records[i][grid.columns[j].field]
           if(!data) data = " "
           line += data
           if(j<grid.columns.length-1) line += ","
       }
       csv += line +"\n"
    }

    var fs = require("fs");
    w2utils.lock($( "#main" ),"Exporting file...",true)
    fs.writeFileSync(selectedPath.toString(), csv);
    w2utils.unlock($( "#main" ))
}