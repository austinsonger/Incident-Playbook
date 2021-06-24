WebDAV = {

    dir: function(url){

        var request = new XMLHttpRequest();

        request.open('PROPFIND', url, false);  // `false` makes the request synchronous
        request.setRequestHeader("Depth", 1)

        request.send(null);

        console.log("Status: " + request.status)
        console.log("XML: " + request.responseText)
        if (request.status === 207) {

            xml = request.responseXML

            elements = xml.getElementsByTagName("D:response")
            for(var i = 0; i<elements.length;i++){

                filename = elements[i].getElementsByTagName("D:href")[0].innerHTML;
                type = elements[i].getElementsByTagName("D:getcontenttype")[0].innerHTML
                console.log("filename: " + filename+"("+type+")")
            }

        }




    },

    read: function(url){

        var request = new XMLHttpRequest();

        request.open('GET', url, false);  // `false` makes the request synchronous

        request.send(null);

        console.log("Status: " + request.status)
        console.log("Response: " + request.responseText)
        if (request.status === 200) {

           content = request.responseText

            console.log(content)

        }

    },

    write: function(url,data){

    },




}