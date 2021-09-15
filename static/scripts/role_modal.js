// Checks if first_login is True and if so shows a modal that can't be closed out until submit
function createRequest(roles, callback) {
    const this_script = $('script[id$="role-modal-script"');
    let user = this_script.attr('data-user').replace(/'/g, '"');
    user = user.replace(/"created_at": .*\, "access_token"/i, "\"access_token\"");
    user = user.replace(/None/g, "\"None\"")
    console.log(user)
    user = JSON.parse(user);

    const data = {};
    const url = `https://api.makerteams.org/users/${user.id}/roles_of_interest/${roles}?token=${user.access_token}`
    console.log(url)
    const request = {
        url: url,
        type: 'PUT',
        data: data,
        success: (res, req) => {
            callback()
        },
        failure: (res, req) => {
            console.log(res, req)
        }
    };

    return request
}

export function create_modal() {
    const modal = $('<div id="role-modal" class="modal fade w-50 p-5" id="rolesModal" tabindex="-1" role="dialog" aria-hidden="true">');
    const dialog = $('<div class="modal-dialog" role="document">');
    const content = $(`<form id="roles-form" class="modal-content" target="">`);
    
    const header = $('<div class="modal-header m-auto">');
    const headerTitle = $('<h5 class="modal-title" id="confirmModalLabel"></h5>').text("Choose Roles");
    const headerClose = $('<button type="button" class="close" data-dismiss="modal" aria-label="Close">').append($('<span aria-hidden="true">').text("&times;"));
    
    const body = $('<div id="form-body" class="modal-body m-auto row align-items-center">');
    const roles = [
        $('<input type="radio" value="front" id="front" name="role">'),
        $('<label for="front" class="p-0 m-1 mr-4">').text("Front-End"),
        $('<input type="radio" value="back" id="back" name="role">'),
        $('<label for="back" class="p-0 m-1 mr-4">').text("Back-End"),
        $('<input type="radio" value="both" id="both" name="role" checked>'),
        $('<label for="both" class="p-0 m-1 mr-4">').text("Both")
    ];

    const footer = $('<div class="modal-footer">');
    const submit = $(`<input type="submit" value="Submit" class="form-control btn col-3 btn-danger">`);

    header.append(headerTitle);
    body.append(...roles);
    footer.append(submit);

    content.append(header, body, footer);
    dialog.append(content);
    modal.append(dialog);

    const options = {
        backdrop: "static",
        keyboard: false,
        focus: true,
        show: false
    };

    modal.modal(options);

    
    modal.submit(e => {
        e.preventDefault()
        const front = $('#front')[0];
        const back =  $('#back')[0];
        const both = $('#both')[0];
        let role = "";

        if (front.checked) role = "Front-End";
        if (back.checked) role = "Back-End";
        if (both.checked) role = "Front-End:Back-End";
        const hide = () => {
            modal.modal('hide');
        }
        const request = createRequest(role, hide);

        $.ajax(request);
        return false;
    });

    modal.on('show.bs.modal', () => {
        console.log('Showing');
    });
    modal.on('shown.bs.modal', () => {
        console.log('Finished showing');
    });
    modal.on('hide.bs.modal', () => {
        console.log('Hiding')
    });
    modal.on('hidden.bs.modal', () => {
        console.log('Finished hiding')
    });

    return modal;
}
