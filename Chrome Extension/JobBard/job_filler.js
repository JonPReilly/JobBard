function ajaxRequest(request_type, request_url, request_data, successFunction)
{
    var r = new XMLHttpRequest();
    r.open(request_type, request_url, true);
    r.onreadystatechange = function () {
    if (r.readyState != 4 || r.status != 200) return "Error";

        successFunction(r.responseText);

    };

    r.send(request_data);
}


function ajaxSuccess(response)
{
    console.log(response);
}

var page_info = {

    "www.facebook.com" : {
        "first_name" : {"type" : "input", "identifier" : {"attr": "placeholder", "val" : "Full Name"}},
    }

}

function getPageInformation(url)
{
    if (url in page_info)
    {
        console.log("in");
        return page_info[url];
    }
    console.log("Not in ");
    return {};
}

function getUserInformation()
{
    return {"first_name" : "Jonathan", "last_name" : "Reilly"};
}

function handleInputField(input_obj, val)
{
    console.log("Handling input");
    console.log(val);
    console.log(input_obj);
    if (input_obj && val &&  input_obj.type !== "hidden" && ( input_obj.value = val ))
            input_obj.style.backgroundColor = "hsla(180, 100%, 50%, 0.15)";
}
function fillForm(page_info, user_info)
{
    Object.keys( page_info ).forEach(function( field ){
        var field_type = page_info[field]["type"];
        var identifier_key = page_info[field]["identifier"]["attr"];
        var identifier_val = page_info[field]["identifier"]["val"];
        var selector = "form " + field_type + "[" +identifier_key +"= '" + identifier_val + "']";
        var input = document.querySelector(selector);

        handleInputField(input, user_info[field]);



    });
}

function onUserInfoRecieved(user_info)
{
    var page_info = getPageInformation(window.location.hostname);
    if (page_info == {}) return;
    if (user_info == {}) return;
    user_info = JSON.parse(user_info);
    fillForm(page_info, user_info);
}
function fillUserJobForm()
{
    ajaxRequest("GET", "http://127.0.0.1:8000/api/jobform", "", onUserInfoRecieved)
}



fillUserJobForm();