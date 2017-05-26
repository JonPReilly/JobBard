

function getUserInfo(responseText)
{
    formFiller.onUserInfoRecieved(responseText);
}

function FormFiller()
{
    this.fillable_inputs = {};
    this.user_info = {};

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
        'email' : /^.*email/i,
        'first_name' : /^.*first.*name/i,
        'last_name' : /^.*last.*name/i,
        'phone_number' : /^.*phone/i
    }
    this.regexMatch = function(input) {
        important_attributes = ['id', 'placeholder', 'name', 'aria-label', 'class']
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
            if (match != "")
                matches[match] = inputs[x];
        }

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

    this.mystery = function() {
        console.log("hello!");
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

var formFiller = new FormFiller();
formFiller.fillForm();