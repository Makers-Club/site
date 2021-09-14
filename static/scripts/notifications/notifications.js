import { getElements } from './utils.js';

const script = $('script[src$="notifications.js"]');
let id = script.attr('data-user_id');
let access_token = script.attr('data-user_access_token');

const url = `https://api.makerteams.org/notifications/${id}?token=${access_token}`;
const { list, button, close, container, iconExample } = getElements();
$(document).ready(() => {

    fetch(url)
    .then(res => res.json())
    .then(data => {
        const { results } = data;
        const ul = $('#notification_list ul');
        for (const item of results) {
            let li;
            const msg = item.msg;
            if (item.is_read) {
                li = $('<li class="notification read text-dark font-weight-normal">').append($(msg));
            }
            else {
                button[0].src = "https://vectr.com/makerteams/dd7C3gKlo.svg?width=640&height=640&select=aFE7U1r8x";
                li = $('<li class="notification unread">').append($(msg));
            }
            ul.append(li);
        } });
        
    const eventUrl = `https://api.makerteams.org/events?token=123123`
    const dashboard = $('#dashboard');
    dashboard.css('border', 'none');
    fetch(eventUrl)
    .then(res => res.json())
    .then(data => {
        const { events } = data;
        const ul = $('#dashboard ul');
        for (const item of events) {
            let li = $('<li class="event h-25 w-25 border">').append($(item.message));
            ul.append(li);
        }
    })


})



// Event Handlers
let flag = 0;
button.click(() => {
    if (flag == 0) {
        //opening - we should send api request telling it these notifications have been read
        list.css('position', 'relative')
        flag = 1;
        fetch(url, {method: 'PUT'})
        .then(res => res.json())
        .then(data => {
            const { status } = data;
        })
    }
    else {
        // closing
        button[0].src = "https://vectr.com/makerteams/dd7C3gKlo.svg?width=640&height=640&select=dd7C3gKlopage0";
        flag = 0;
        let unreads = document.getElementsByClassName("unread");
        for (let i = 0; i < unreads.length; i++) {
            console.log(unreads[i])
            unreads[i].classList.remove("unread");
          }
    } 
});

iconExample.click(() => {
    if (flag == 1) {
        list.css('display', 'none');
        button[0].src = "https://vectr.com/makerteams/dd7C3gKlo.svg?width=640&height=640&select=dd7C3gKlopage0";
        flag = 0;
    }
});


const createbtn = $('#create_btn');
createbtn.click(() => {

    const projUrl = `http://127.0.0.1:8081/projects?token=123123&name=ProjectX&short_description=somedescriptionhere&repository_link=google&owner_handle=${id}&repository_name=somereponame&owner=${id}`
    fetch(projUrl, {method: 'POST'})
    .then(res => {res.json(); console.log(res)})
    .then(data => {
        console.log(data)
    })
})

