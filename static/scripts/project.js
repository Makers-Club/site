

const createSprint = $('#create_sprint');
const script = $('script[src$="notifications.js"]');
let id = script.attr('data-user_id');
let access_token = script.attr('data-user_access_token');
let handle = script.attr('data-user_handle');
console.log(createSprint)
$(document).ready(() => {
})
const url = `https://api.makerteams.org/sprint?token=${access_token}`

createSprint.click(() => {
    console.log('requesting create sorint')
    fetch(url, {
        method: "POST"
    })
    .then(res => res.json())
    .then(data => {
        if (data) {
            console.log(data)
            const { sprint } = data;
            const ul = $('#sprints');
            if (sprint) {
                
                        li = $('<li class="sprint">');
                        li.prepend($(sprint));
            }
            else {
                console.log(url);
                console.log(data);
            }
        }
    });
});