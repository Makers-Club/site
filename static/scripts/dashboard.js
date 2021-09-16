const script = $('script[src$="dashboard.js"]');
let id = script.attr('data-user_id');
let access_token = script.attr('data-user_access_token');
let handle = script.attr('data-user_handle');

$(document).ready(() => {
    console.log(access_token)

const eventUrl = `https://api.makerteams.org/events?token=${access_token}`
const dashboard = $('#dashboard');
dashboard.css('border', 'none');
fetch(eventUrl)
.then(res => res.json())
.then(data => {
    if (data) {
        const { events } = data;
        if (events) {
            const ul = $('#dashboard ul');
            
            events.sort(function (a, b) {
                return parseInt(a.id) < parseInt(b.id);
            })
            events.reverse()


            for (let i = 0; i < events.length; i++) {
                console.log(events[i])
                let msg = events[i].message
                let li = $('<li class="rounded my-3 bg-dark w-100 p-2 event">');
                let div = $('<div class="lighter p-2 rounded">');
                div.append(msg);
                li.append(div);
                ul.append(li);
            }
        }
        else {
            console.log(eventUrl)
            console.log('***', data)
            location.reload()
        }
    
    }
})
})