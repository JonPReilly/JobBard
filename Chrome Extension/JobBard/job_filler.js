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


function getPageInformation()
{
    var page_info = {
        "first_name" : {"type" : "input", "identifier" : {"attr": "id", "val" : "inputSuccess2"}},
        "last_name" : {"type" : "input", "identifier" : {"attr": "id", "val" : "inputSuccess3"}}
    };
    return page_info;
}

function getUserInformation()
{
    return {"first_name" : "Jonathan", "last_name" : "Reilly"};
}

function fillForm(page_info, user_info)
{
    Object.keys( page_info ).forEach(function( field ){
        var field_type = page_info[field]["type"];
        var identifier_key = page_info[field]["identifier"]["attr"];
        var identifier_val = page_info[field]["identifier"]["val"];
        var selector = "form " + field_type + "[" +identifier_key +"= '" + identifier_val + "']";
        var input = document.querySelector(selector);


        if (input && user_info[ field ] &&  input.type !== "hidden" && ( input.value = user_info[ field ] ))
            input.style.backgroundColor = "hsla(180, 100%, 50%, 0.15)";


    });
}
function fillUserJobForm()
{
    var page_info = getPageInformation();
    if (page_info == {}) return;
    var user_info = getUserInformation();
    if (user_info == {}) return;

    fillForm(page_info, user_info);
}



fillUserJobForm();