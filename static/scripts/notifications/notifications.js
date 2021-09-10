import { getUser, getElements } from './utils.js';

const user = getUser();
const { access_token, avatar, credits, email, handle, id, name, projects, roles_of_interest } = user;
const url = `https://api.makerteams.org/notifications/${id}?token=${access_token}`;
const { list, button, close, container } = getElements();

$(document).ready(() => {
    fetch(url)
    .then(res => res.json())
    .then(data => {
        const { results } = data;
        const ul = $('#notification_list ul');

        for (const item of results) {
            if (item.is_read) continue;
            const msg = item.msg;
            const li = $('<li>').append($(msg));
            ul.append(li);
        }   
    });
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
