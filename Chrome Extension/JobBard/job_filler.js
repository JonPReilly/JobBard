function ajaxRequest(request_type, request_url, request_data)
{
    var r = new XMLHttpRequest();
    r.open(request_type, request_url, true);
    r.onreadystatechange = function () {
    if (r.readyState != 4 || r.status != 200) return "Error";

        ajaxSuccess(r.responseText);

    };

    r.send(request_data);
}


function ajaxSuccess(response)
{
    console.log(response);
}
var res = ajaxRequest("GET", "http://127.0.0.1:8000/", "");

