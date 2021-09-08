export function mockPing(user_id, access_token) {
    const data = {
        "status": "OK",
        "results": [
            { "id": 1, "user_id": user_id, "msg": "This is a message", "is_read": "False" },
            { "id": 2, "user_id": user_id, "msg": "This is a message", "is_read": "True" }
        ]
    }
    const res = {
        json: () => (data["status"] === "OK") ? data["results"] : undefined
    }

    return res; 
}

export function getUser() {
    const script = $('script[src$="notifications.js"]');
    let userData = script.attr('data-user');
    userData = userData.replace(/None/g, '"None"');
    userData = userData.replace(/'/g, '"');
    userData = userData.replace(/"created_at": .*\, "access_token"/i, '"access_token"');
    return JSON.parse(userData);
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
