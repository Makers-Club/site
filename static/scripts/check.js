function check(user, repo) {
    $.ajax({
        url: 'http://127.0.0.1:8080/api/checker',
        type: 'post',
        data: {user: user, repo: repo},
        dataType: 'json',
        success: function (data) { $("#target").html( data.string ) },
        fail: function(jqXHR, text, error) { alert(text) }
    });
};
