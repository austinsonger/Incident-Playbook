function misp_connection_test(){


    mispserver = w2ui.case_form.record['mispserver']
    mispapikey = w2ui.case_form.record['mispapikey']
    mispeventid = w2ui.case_form.record['mispeventid']

    $.ajaxSetup({
        headers:{
            'Authorization': mispapikey,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    });

    url = mispserver+"/events/"+mispeventid

    $.ajax(url,
        {
            dataType: 'json', // type of response data
            timeout: 5000,     // timeout milliseconds
            success: function (data,status,xhr) {



                alert("Test OK. You'll be sending to the event '" + data.Event.info +"'");
            },
            error: function (xhr, textStatus, errorMessage) { // error callback

                if(xhr.status == 403) {

                    var details = ""
                    if(xhr.responseJSON.errors) details = xhr.responseJSON.errors.value[0]
                    alert(xhr.responseJSON.message +" "+ details)
                    return
                }

                if(xhr.status == 404) {
                    alert("Event ID/UUID not found!")
                    return
                }

                if(xhr.status != 200 ) {
                    alert("Connection Error! Is MISP running there?")
                    return
                }

                alert("Connection Error! Check Server Address.")
                return
            }
        });

}


/**
 * Add selected attributes to misp
 * @param grid - source grid
 * @param selection - selection array
 */
function add_attributes_misp(grid,selection){ //TODO: get rid oof selectioon and get it from grid object in this function

    grid.save()
    mispserver = case_data.mispserver
    mispapikey = case_data.mispapikey
    mispeventid = case_data.mispeventid

    if(!(mispserver && mispapikey && mispeventid)){
        alert("Please configure correct MISP creds under Case Details first.")
    }

    // That's how a misp event looks like
    //{"value":"1.2.3.4","type":"ip-dst"}

    misp_object = []
    for(var i=0; i< selection.length; i++){

        var record = grid.get(selection[i])

        comment = ""
        if(record.comment) comment = record.comment
        var entry = {"value":String(record.value),"type":String(record.misp_field_type),"comment":comment}
        misp_object.push(entry)

    }

    if(misp_object.length == 0){
        alert("You need to select at least one indicator.")
        return
    }

    $.ajaxSetup({
        headers:{
            'Authorization': mispapikey,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    });



    url = mispserver+"/attributes/add/"+mispeventid

    $.ajax(url,
        {
            dataType: 'json', // type of response data
            data: JSON.stringify(misp_object),
            method:"POST",
            timeout: 5000,     // timeout milliseconds
            success: function (data,status,xhr) {

                w2popup.close()
                if(misp_object.length == 1) {
                    alert("Successfully added " + misp_object.length + " attribute to the configured MISP event.");
                }
                else {
                    alert("Successfully added " + misp_object.length + " attributes to the configured MISP event.");
                }
            },
            error: function (xhr, textStatus, errorMessage) { // error callback

                if(xhr.status == 403) {

                    var details = ""
                    if(xhr.responseJSON.errors) details = xhr.responseJSON.errors.value[0]
                    alert(xhr.responseJSON.message +" "+ details)
                    return
                }

                if(xhr.status == 404) {
                    alert("Event ID/UUID not found!")
                    return
                }

                if(xhr.status != 200 ) {
                    alert("Connection Error! Is MISP running there? "+errorMessage)
                    return
                }

                alert("Connection Error! Check Server Address.")
                return
            }
        });

}


//curl --header "Authorization: YOUR API KEY " --header "Accept: application/json" --header "Content-Type: application/json" -d "{"event_id":"3542","value":"1.2.3.4","category":"Network activity","type":"ip-dst"}" http://10.50.13.60/attributes/add/3542