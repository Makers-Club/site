const script = $('script[src$="project.js"]');



let createSprint = $('#create_sprint');
let markSprintComplete = $('#mark_sprint_complete')
let id = script.attr('data-user_id');
let access_token = script.attr('data-user_access_token');
let handle = script.attr('data-user_handle');
let project_id = script.attr('data-project_id');
let currentSprintId = script.attr('data-current_sprint')

console.log(handle)
console.log(project_id)
console.log(currentSprintId, 'HEY')


const url = `https://api.makerteams.org/sprints?token=${access_token}&project_id=${project_id}&owner_handle=${handle}`
console.log(url)

createSprint.click(() => {
    fetch(url, {
        method: "POST"
    })
    .then(res => res.json())
    .then(data => {
        if (data) {
            const { sprint } = data;
            let ul = $('#sprints');
            if (sprint) {

                
                location.reload();

            }
            else {
                alert('no sprint')
                console.log(url);
                console.log(data);
            }
            console.log('SPRINT CREATED')
        }
    });
});


const sprintDoneurl = `https://api.makerteams.org/sprints/${currentSprintId}?token=${access_token}&complete=1`
console.log(sprintDoneurl)
markSprintComplete.click(() => {
    console.log('IN HERE YO')
    fetch(sprintDoneurl, {
        method: "PUT"})
    .then(res => res.json())
    .then(data => {
        const { sprint } = data;
        if (sprint) {
            console.log(data)
            location.reload();
        }
        else {
            console.log(data)
        }

    })
});
        




