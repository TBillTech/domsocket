//Copyright (c) 2015 TBillTech.  

//This Source Code Form is subject to the terms of the Mozilla Public
//License, v. 2.0. If a copy of the MPL was not distributed with this
//file, You can obtain one at http://mozilla.org/MPL/2.0/.

var summary = {"__Summary__": true, "test_count": 0, "success_count": 0, "errors": null}

var page = require('webpage').create();

function assert(condition) {
    summary.test_count += 1;
    if (condition)
    {
	summary.success_count += 1;
    }
    else
    {
        throw Error("Assert");
    }
}

function assert_equal(value, equal_to) {
    summary.test_count += 1;
    if (value === equal_to)
    {
	summary.success_count += 1;
    }
    else
    {
        throw Error("Assert Equal: " + JSON.stringify(value) + " == " + JSON.stringify(equal_to));
    }
}

function assert_equal_nocase(value, equal_to) {
    summary.test_count += 1;
    if (value.toUpperCase() === equal_to.toUpperCase())
    {
	summary.success_count += 1;
    }
    else
    {
        throw Error("Assert Equal Case Insensitive: " + JSON.stringify(value) + " == " + JSON.stringify(equal_to));
    }
}

function get_text_content_of(id) {
    return get_element_by_id_on_page(id).textContent;
}

function get_attribute_of(id, attribute) {
    return get_element_by_id_on_page(id).getAttribute(attribute);
}

function get_tag_of(id) {
    return get_element_by_id_on_page(id).tagName;
}

function get_element_by_id_on_page(id) {
    return page.evaluate(function(id_value) {
        return document.getElementById(id_value);
    }, id);
}

function has_attribute(id, attribute) {
    return get_element_by_id_on_page(id).hasAttribute(attribute);    
}

function has_id(id) {
    var element =  get_element_by_id_on_page(id);
    if (typeof(element) != 'undefined' && element != null)
    {
        return true;
    }
    return false;
}


function do_test(timeout, test_function) {
    setTimeout(function(do_test) {
    	try
        {
            do_test();
        }
        catch(err)
        {
	    if(err.hasOwnProperty('stack'))
	    {
	        summary.errors = [err.message, JSON.stringify(err.stack)];
	    }
	    else
	    {
		summary.errors = [err.message, 'Test failed'];
	    }
            console.log(JSON.stringify(summary));
            phantom.exit();
	    throw err;            
        }
    }, timeout, test_function);
}

function do_final_test(timeout, test_function) {
    setTimeout(function(do_test) {
    	try
        {
            do_test();
        }
        catch(err)
        {
	    if(err.hasOwnProperty('stack'))
	    {
	        summary.errors = [err.message, JSON.stringify(err.stack)];
	    }
	    else
	    {
		summary.errors = [err.message, 'Test failed'];
	    }
	    throw err;            
        }
	finally
        {
            console.log(JSON.stringify(summary));
            phantom.exit();

        }
    }, timeout, test_function);
}

page.open('https://10.0.0.8:8443', function(status) {

    if (status !== 'success') {
	summary.errors = ['FAIL to load the address'];
	console.log(JSON.stringify(summary));
        phantom.exit();
    } else {
	run_test();
    }
});




