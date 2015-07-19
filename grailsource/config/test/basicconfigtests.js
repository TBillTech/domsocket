
function run_test() {
    do_test(500, groupA_tests);
}

function groupA_tests() {
    all_basic_config_tests('config');
}

function all_basic_config_tests(id) {
    login_dialog_test(id+'.login');
}

function login_dialog_test(id) {
    var username = get_element_by_id_on_page(id+'.loginDialog.0.1.0.0.username');
    var password = get_element_by_id_on_page(id+'.loginDialog.0.1.0.1.password');
    username.value = 'bad';
    password.value = 'bee';
    var login_button = get_element_by_id_on_page(id+'.loginDialog.0.1.0.2.loginButton');
    assert_equal(get_text_content_of(id+'.loginDialog.0.1.0.2.loginButton'), 'Login');
    login_button.click();
    do_test(100, function(elid) { login_dialog_test_2(elid); }.bind(null, id));
}

function login_dialog_test_2(id) {
    assert_equal(get_text_content_of('config.invalid'), 'username and/or password is invalid');
    var username = get_element_by_id_on_page(id+'.loginDialog.0.1.0.0.username');
    var password = get_element_by_id_on_page(id+'.loginDialog.0.1.0.1.password');
    username.value = 'tester';
    password.value = ':testPa$s*@134~!';
    var login_button = get_element_by_id_on_page(id+'.loginDialog.0.1.0.2.loginButton');
    login_button.click();
    do_final_test(100, function(elid) { login_dialog_test_3(elid); }.bind(null, id));
}

function login_dialog_test_3(id) {
    assert(!has_id('config.invalid'));
}
