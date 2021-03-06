//Copyright (c) 2015 TBillTech.  

//This Source Code Form is subject to the terms of the Mozilla Public
//License, v. 2.0. If a copy of the MPL was not distributed with this
//file, You can obtain one at http://mozilla.org/MPL/2.0/.

function run_test() {
    do_test(800, groupA_tests);
}

function groupA_tests() {
    all_basic_tester_tests('tester');
}

function all_basic_tester_tests(id) {
    first_paragraph_test(id+'.first_paragraph');
    sub_body_test(id+'.sub_body');
    login_dialog_test(id+'.login');
}

function first_paragraph_test(id) {
    assert_equal_nocase(get_tag_of(id), 'p');
    assert_equal(get_text_content_of(id), 'Hello World! -- changed!');
    assert_equal(get_attribute_of(id, 'class'), 'first');
    assert(!has_attribute(id,'toremove'));
}

function sub_body_test(id) {
    assert_equal_nocase(get_tag_of(id), 'body');
    assert_equal(get_attribute_of(id,'class'), 'sub_body_class');
    sub_paragraph_test(id+'.subp_child');
    sub_body_divA_test(id+'.sub_body_divA');
    assert(!has_id(id+'.sub_body_divB'));
} 

function sub_paragraph_test(id) {
    assert_equal_nocase(get_tag_of(id), 'p');
    assert_equal(get_text_content_of(id), 'Hello World! -- from the sub paragraph');
}

function sub_body_divA_test(id) {
    assert_equal_nocase(get_tag_of(id), 'div');
    assert_equal_nocase(get_tag_of(id+'.0'), 'div');
    assert(!has_id(id+'.1'));
    assert_equal_nocase(get_tag_of(id+'.2'), 'p');
    assert_equal_nocase(get_tag_of(id+'.17'), 'span');
    assert_equal_nocase(get_tag_of(id+'.18'), 'li');
    assert_equal_nocase(get_tag_of(id+'.19'), 'span');
    assert_equal_nocase(get_tag_of(id+'.5'), 'div');
    assert_equal_nocase(get_tag_of(id+'.6'), 'div');
    assert_equal_nocase(get_tag_of(id+'.21'), 'p');
    assert_equal_nocase(get_tag_of(id+'.8'), 'div');
    assert_equal_nocase(get_tag_of(id+'.22'), 'p');
    assert_equal_nocase(get_tag_of(id+'.10'), 'div');
    assert_equal_nocase(get_tag_of(id+'.23'), 'p');
    assert_equal_nocase(get_tag_of(id+'.12'), 'div');
    assert_equal_nocase(get_tag_of(id+'.13'), 'div');
    assert_equal_nocase(get_tag_of(id+'.15'), 'div');
    assert_equal_nocase(get_tag_of(id+'.20'), 'span');
    assert_equal(get_attribute_of(id, 'custom_class'), 'custom_class_info');
    assert_equal(get_attribute_of(id, 'keyword2'), 'keyword2_info');
}

function login_dialog_test(id) {
    var username = get_element_by_id_on_page(id+'.myLoginDialog.0.1.0.0.username');
    var password = get_element_by_id_on_page(id+'.myLoginDialog.0.1.0.1.password');
    username.value = 'bad';
    password.value = 'bee';
    var login_button = get_element_by_id_on_page(id+'.myLoginDialog.0.1.0.2.loginButton');
    assert_equal(get_text_content_of(id+'.myLoginDialog.0.1.0.2.loginButton'), 'Login');
    login_button.click();
    do_test(400, function(elid) { login_dialog_test_2(elid); }.bind(null, id));
}

function login_dialog_test_2(id) {
    assert_equal(get_text_content_of('tester.invalid'), 'username and/or password is invalid');
    var username = get_element_by_id_on_page(id+'.myLoginDialog.0.1.0.0.username');
    var password = get_element_by_id_on_page(id+'.myLoginDialog.0.1.0.1.password');
    username.value = 'bee';
    password.value = 'bad';
    var login_button = get_element_by_id_on_page(id+'.myLoginDialog.0.1.0.2.loginButton');
    login_button.click();
    do_test(200, function(elid) { login_dialog_test_3(elid); }.bind(null, id));
}

function login_dialog_test_3(id) {
    assert_equal(get_text_content_of('tester.valid'), 'username and password is valid');
    var login_button = get_element_by_id_on_page(id+'.myLoginDialog.0.1.0.2.loginButton');
    login_button.click();
    do_test(200, function(elid) { login_dialog_test_4(elid); }.bind(null, id));
}

function login_dialog_test_4(id) {
    assert_equal(get_attribute_of('tester.valid', 'style'), 'color:green');
    do_test(0, function() { increment_widget_test(); }.bind(null));
}

function increment_widget_test() {
    var incrementor = get_element_by_id_on_page('tester.incrementor');
    assert_equal(get_attribute_of('tester.incrementor', 'haveWork'), 'false');
    assert_equal(get_attribute_of('tester.incrementor', 'currentValue'), '3');
    incrementor.setAttribute('haveWork', 'true');
    do_final_test(200, function() { increment_widget_test_2(); }.bind(null));
}

function increment_widget_test_2() {
    assert(!has_id('tester.incrementor'));
    assert_equal(get_attribute_of('tester', 'incrementor_destroyed'), 'true');
}
