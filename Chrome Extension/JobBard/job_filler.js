//https://cs.chromium.org/chromium/src/components/autofill/core/browser/

function getUserInfo(responseText)
{
    formFiller.onUserInfoRecieved(responseText);
}

function FormFiller()
{
    this.declineToIdentifyRegex = /^.*(decline to|don\'t)/i;
    this.selectionMapping = {
        'veteran_status' : {
            'N' : /^.*(no|am not)/i,
            'Y' : /^(?!.*(not|no|select)).*(identify)/i,
            'D' : this.declineToIdentifyRegex ,
        },
        'gender' : {
            'M' : /^(?!.*(fe)).*(male)/i,
            'F' : /^.*female.*/i,
            'D' : this.declineToIdentifyRegex ,
        },
        'disability_status' : {
            'N' : /^.*(no)/i,
            'Y' : /^.*(yes)/i,
            'D' : this.declineToIdentifyRegex ,

        }
    }
    this.regularExpressions = {
        'full_name' : /^(?!.*(first|last|account|user|given|family|mid|login)).*name/i,
        'email' : /^.*email/i,
        'first_name' : /^(?!.*(login|user)).*(first|given|f).*name/i,
        'last_name' : /^(?!.*(login|user)).*(last|family|l).*name/i,
        'phone_number' : /^.*(phone|tel)/i,
        'zip' : /^.*(zip|postal)/i,
        'city' : /^.*city/i,
        'street_address' : /^(?!.*(city|state|country)).*address(?!.*(2)).*/i,
        'github' : /^.*github.*/i,
        'linkedin' : /^.*linkedin.*/i,
        'state' : /^(?!.*(united)).*(state|county|region)/i,
        'veteran_status' : /^.*veteran.*/i,
        'gender' : /^.*(gender|sex).*/i,
        'disability_status' : /^.*(disability|handicap).*/i
    }
    this.probable_job_form = false;
    this.inputs_filled_for_probable_job_form = 3;
    this.fillable_inputs = {};
    this.user_info = {};

    this.setElementBackgroundColor = function(element) {
        element.style.backgroundColor = "hsla(180, 100%, 50%, 0.15)";
    }

    this.handleElementChange = function(element, val, attribute_key) {
        var element_type = element.tagName;
        switch(element_type) {
            case "INPUT":
                this.handleInputField(element,val);
                break;
            case "SELECT":
                this.handleSelectInput(element,val,attribute_key);
                break;
            default:
                return;

        }
        this.setElementBackgroundColor(element);
    }

    this.handleRadioInput = function(element) {
        element.checked = true;
    }
    this.handleTextInput = function(element, val)
    {
        element && val &&  element.type !== "hidden" && ( element.value = val )
    }
    this.handleOptionInput = function(option)
    {
        option.selected = true;
    }
    this.handleSelectInput = function(select, user_value, attribute_key)
    {
        console.log("SELECT INPUT FIELD : " , select);
        if (!(attribute_key in this.selectionMapping))
            return;
        console.log(attribute_key, user_value, attribute_key in this.selectionMapping)
        var option_selection_regex = this.selectionMapping[attribute_key][user_value];
        var options = select.options;
        for(x=1; x<options.length; x++)
        {
            console.log(options[x].innerText, option_selection_regex,option_selection_regex.test(options[x].innerText) );
            if(option_selection_regex.test(options[x].innerText))
            {
                this.handleOptionInput(options[x]);
                return;
            }
        }
    }
    this.handleInputField = function(element, val)
    {
        var input_type = element.type;
        switch(input_type) {
           case "text":
           case "url":
           case "email":
                this.handleTextInput(element,val);
                break;
           case "radio":
                this.handleRadioInput(element);
           default:
                break;

        }

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
                    return field_match;
            }
        }

        return "";
    }
    this.findAllLabels = function() {
        var labels = document.getElementsByTagName("label");
        return labels;
    }
    this.findAllSelects = function() {
        var selects = document.getElementsByTagName("select");
        return selects;
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

            this.handleElementChange(this.fillable_inputs[key], this.user_info[key], key);
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
    this.getFillableFields = function() {
        var elems = document.querySelectorAll("select,input");
        return elems;
    }
    this.fillForm = function() {
        fillable_fields = this.getFillableFields();
        this.fillable_inputs = this.regexMatchInputs(fillable_fields);
        this.getUserInformation("GET", "http://127.0.0.1:8000/api/jobform", "", getUserInfo);

    }
}

console.log("******************* JobBard ***********************");
var formFiller = new FormFiller();
formFiller.fillForm();


console.log("**************************************************");



/*
MutationObserver = window.MutationObserver || window.WebKitMutationObserver;






MutationObserver = window.MutationObserver || window.WebKitMutationObserver;

var observer = new MutationObserver(function(mutations, observer) {
    // fired when a mutation occurs
    console.log("Muation occured");
    console.log(mutations.type);
    console.log(mutations);


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
