function check(user, repo) {
    $.ajax({
        url: 'http://127.0.0.1:8080/api/checker',
        type: 'post',
        data: {user: user, repo: repo},
        dataType: 'json',
        success: display_checks,
        fail: function(jqXHR, text, error) { console.log(text) }
    });
};

/**
 * From J.I. to others:
 * This function is solely meant to serve as an example for how to use the
 * incoming `checks` list from the Checker API. Please create something better
 * than this.
 */
function display_checks(data) {
    
    let checks = data.checks;
    let str = 'Results:';
    
    /**
     * `checks` is a list of `check` dictionaries
     * 
     * this is the schema for the `check` dictionary:
     * {
     *  'description': str # check description
     *  'result': bool # True if check passed, False if check failed
     *  'message': str # message for user
     *  'check_id': int # check number
     *  'check_type': str # e.g. requirement, output, pytest, etc
     *  'stdout': str # checker output
     *  'stderr': str # checker error
     * }
     * 
     * if no checks were returned, the checker API is down
     */

    if (!checks) {
        $("#checks").html('Something went wrong on our end. Retry later.');
        return;
    }
    console.log(checks);
    /* Here's one example for how you could use some of its attributes */
    for (let check of checks) {
        str += `</br>
        Check ${check.check_id}: ${check.description}
        ${check.result ? '✅' : '❌'} --- ${check.message}
        `;
    }
    $("#checks").html(str);
}
