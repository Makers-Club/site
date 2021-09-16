
const script = $('script[src$="projects.js"]');
let id = script.attr('data-user_id');
let access_token = script.attr('data-user_access_token');
let handle = script.attr('data-user_handle');
let user_pic = script.attr('data-user_pic')


$(document).ready(() => {

const createbtn = $('#create_btn');
createbtn.click(() => {
    const projUrl = `http://127.0.0.1:8081/projects?token=123123&name=Project%20X&short_description=somedescriptionhere&repository_link=google&owner_handle=${handle}&repository_name=somereponame&owner=${handle}&user_pic=${user_pic}`
    console.log(projUrl)
    fetch(projUrl, {method: 'POST'})
    .then(res => res.json())
    .then(data => {
        console.log("IN PROJECTS ALL PAGE")
    })
})
});