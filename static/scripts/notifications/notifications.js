import { getUser, getElements, mockPing } from './utils.js';

const user = getUser();
const { access_token, avatar, credits, email, handle, id, name, projects, roles_of_interest } = user;
const url = `https://api.makerteams.org/notifications/${id}?token=${access_token}`;
const { list, button, close, container } = getElements();

const mock = () => {
    const res = mockPing(id, handle, access_token);
    const data = res.json();
    const ul = $('#notification_list ul');

    for (const item of data) {
        if (item.is_read === "true") continue;
        const msg = item.msg;
        const li = $('<li>').append($(msg));
        ul.append(li);
    }
};

$(document).ready(() => {
    // fetch(url, (res) => {
    //     const data = res.json();
    //     const ul = $('#notification_list ul');

    //     for (const item of data) {
    //         if (item.is_read === "true") continue;
    //         const msg = item.msg;
    //         const li = $('<li>').append($(msg));
    //         ul.append(li);
    //     }   
    // });
    mock();
});


// Event Handlers

button.click(() => {
    button.css('display', 'none');
    list.css('display', 'block');
    container.toggleClass('border bg-white');
});

close.click(() => {
    button.css('display', 'block');
    list.css('display', 'none');
    container.toggleClass('border bg-white');
});
