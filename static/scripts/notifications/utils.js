export function mockPing(user_id, user_handle, access_token) {
    const data = {
        "results": [
            {
            "id": "1", 
            "is_read": false, 
            "msg": `<p><a href='https://api.makerteams.org/users/${user_handle}?token=123123' target='_blank'>${user_handle}</a> has invited you to work on a project: <a href='https://www.google.com' target='_blank'>link</a></p>`, 
            "user_id": `${user_id}`
            }
        ], 
        "status": "OK"
}
    const res = {
        json: () => (data["status"] === "OK") ? data["results"] : undefined
    }

    return res; 
}

export function getElements() {
    const list = $('#notification_list');
    const button = $('#notification_button');
    const close = $('#notification_list_close');
    const container = $('#notifications');

    close.css('position', 'absolute');
    close.css('top', '.5rem');
    close.css('right', '.5rem');
 
    return { list, button, close, container };
}
 