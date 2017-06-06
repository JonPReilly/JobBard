

function getUserInfo(responseText)
{
    formFiller.onUserInfoRecieved(responseText);
}

function FormFiller()
{
    this.probable_job_form = false;
    this.inputs_filled_for_probable_job_form = 3;
    this.fillable_inputs = {};
    this.user_info = {};

    this.handleSelectField = function() {
        document.getElementById("job_application_veteran_status").selectedIndex = "1";
    }
    this.handleCheckboxField = function() {

    }
    this.handleInputField = function(input_obj, val)
    {

        if (input_obj && val &&  input_obj.type !== "hidden" && ( input_obj.value = val ))
           input_obj.style.backgroundColor = "hsla(180, 100%, 50%, 0.15)";
    }

    this.getElementAttributes = function(element, attributes)
    {
        var attribute_values = [];
        for(var x=0; x< attributes.length; x++)
        {
            value = element.getAttribute(attributes[x])
            if(value != null)
                attribute_values.push(value);
        }
        return attribute_values;
    }
    this.regularExpressions = {
        'full_name' : /^(?!.*(first|last|account|user|given|family|middle)).*name/i,
        'email' : /^.*email/i,
        'first_name' : /^.*(first|given|f).*name/i,
        'last_name' : /^.*(last|family|l).*name/i,
        'phone_number' : /^.*(phone|tel)/i,
        'zip' : /^.*(zip|postal)/i,
        'city' : /^.*city/i,
        'street_address' : /^(?!.*(city|state|country)).*address(?!.*(2)).*/i,
        'github' : /^.*github.*/i,
        'linkedin' : /^.*linkedin.*/i
    }
    this.regexMatch = function(input) {
        if(input.type == "hidden")
            return "";
        important_attributes = ['id', 'placeholder', 'autocomplete' , 'name', 'aria-label', 'class']
        element_attributes = this.getElementAttributes(input, important_attributes);

        for(var x=0; x< element_attributes.length; x++)
        {
            for (field_match in this.regularExpressions)
            {
                if(this.regularExpressions[field_match].test(element_attributes[x]))
                    return field_match
            }
        }

        return "";
    }

    this.findAllInputs = function() {
        var inputs = document.getElementsByTagName("input");
        return inputs;
    }

    this.regexMatchInputs = function(inputs) {
        var matches = {};
        for(var x=0; x< inputs.length; x++)
        {
            match = this.regexMatch(inputs[x]);
            if (match != "" && !(match in matches))
                matches[match] = inputs[x];
        }
        console.log("Matches: " , matches);
        if(matches.length > this.inputs_filled_for_probable_job_form)
            this.probable_job_form = true;
        return matches;
    }

    this.inputUserInformation = function() {
        if (this.fillable_inputs == {} || this.user_info == {})
            return;

        for (key in this.fillable_inputs)
        {
            this.handleInputField(this.fillable_inputs[key], this.user_info[key]);
        }
    }

    this.onUserInfoRecieved = function(user_info)
    {
        this.user_info = JSON.parse(user_info);
        this.inputUserInformation();

    }



    this.getUserInformation = function(request_type, request_url, request_data, callback) {
        var r = new XMLHttpRequest();
        r.open(request_type, request_url, true);
        r.onreadystatechange = function () {
        if (r.readyState != 4 || r.status != 200) return "Error";



            callback(r.responseText);

        };
        r.send(request_data);
    }
    this.fillForm = function() {
        all_inputs = this.findAllInputs();
        this.fillable_inputs = this.regexMatchInputs(all_inputs);
        this.getUserInformation("GET", "http://127.0.0.1:8000/api/jobform", "", getUserInfo);

    }
}

console.log("******************* JobBard ***********************");
var formFiller = new FormFiller();
formFiller.fillForm();

console.log(document.location.toString());
console.log(document.referrer);
console.log("**************************************************");
/*
var formFiller = new FormFiller();
formFiller.fillForm();



MutationObserver = window.MutationObserver || window.WebKitMutationObserver;

var observer = new MutationObserver(function(mutations, observer) {
    // fired when a mutation occurs
    formFiller.fillForm();


    // ...
});

// define what element should be observed by the observer
// and what types of mutations trigger the callback
observer.observe(document, {
  subtree: true,
  attributes: true
  //...
});
*/


// https://stackoverflow.com/questions/41225975/access-dom-elements-inside-iframe-from-chrome-extension
// https://stackoverflow.com/questions/6570363/chrome-extension-content-scripts-and-iframe
