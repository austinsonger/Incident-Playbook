function vt_connection_test(){


    vtapikey = w2ui.case_form.record['vtapikey']

    if(!vtapikey){
        alert("Please specify an API key first.")
        return
    }


    $.ajaxSetup({
        headers:{
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    });

    url = "https://www.virustotal.com/vtapi/v2/file/report?apikey="+vtapikey+"&resource=a7f7a0f74c8b48f1699858b3b6c11eda"

    $.ajax(url,
        {
            dataType: 'json', // type of response data
            timeout: 5000,     // timeout milliseconds
            success: function (data,status,xhr) {

                alert("Test OK. VT Connected...");
            },
            error: function (xhr, textStatus, errorMessage) { // error callback

                if(xhr.status == 403) {

                    alert("Your API key seems to be invalid.")
                    return
                }
                    alert("Connection Error!")
                    return
            }
        });
}



function check_vt(grid, recid){

    vtapikey = case_data.vtapikey
    ressource = grid.get(recid).md5

    if(!vtapikey){
        alert("Please specify an API key first under Case Settings.")
        return
    }


    $.ajaxSetup({
        headers:{
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    });



    url = "https://www.virustotal.com/vtapi/v2/file/report?apikey="+vtapikey+"&resource="+ressource

    $.ajax(url,
        {
            dataType: 'json', // type of response data
            timeout: 5000,     // timeout milliseconds
            success: function (data,status,xhr) {

                if(data.response_code == 1 && data.positives > 0) {
                    grid.set(recid,{vt:"infected"})
                }
                else if(data.response_code==1 && data.positives==0){
                    grid.set(recid,{vt:"clean"})
                }
                else {
                    grid.set(recid, {vt: "noresult"})
                }

            },
            error: function (xhr, textStatus, errorMessage) { // error callback

                if(xhr.status == 403) {

                    alert("Your API request rate seems to be exceeded. Try again later or change API key.")
                    return
                }
                if(xhr.status == 204) {

                    alert("Your API key seems to be invalid.")
                    return
                }

                alert("Connection Error!")
                return
            }
        });
}