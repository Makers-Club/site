const roles = [
    'Front-End',
    'Back-End',
];
let filter_values = ['all'];

function handleOnChange(value) {
    if (filter_values.includes(value)) filter_values.splice(filter_values.indexOf(value), 1);
    else filter_values.push(value);

    updateUsers(filter_values);
}

function updateUsers(filter_values) {
    const users = $('section div.user-card');
    for (const user of users) {
        const userRoles = user.getAttribute('data-role').split(':');

        if (filter_values.length === 0) {
            user.style.display = 'none';
            continue;
        }
        if (filter_values.includes('all')) {
            user.style.display = 'block';
            continue;
        }

        user.style.display = 'none';
        for (const role of userRoles) {
            if (filter_values.includes(role)) {
                user.style.display = 'block';
                break;
            }
        }
    }
}

// list is an ul element
export function loadUsersFilter(list) {
    const inputs = [
        {
            label: $('<label class="m-0" for="cb_show_all">Show All</label>'),
            input: $('<input class="ml-1 filter_item" type="checkbox" id="cb_show_all" value="all" checked />')
        }
    ];
    inputs[0].input.change(() => { handleOnChange('all') });

    for (const role of roles) {
        const role_id = `cb_${role}`;
        const item = {
            label: $(`<label class="m-0" for="${role_id}">${role}</label>`),
            input: $(`<input class="filter_item ml-1" type="checkbox" id="${role_id}" value="${role}" />`)
        };

        item.input.change(() => { handleOnChange(role) });
        inputs.push(item);
    }

    for (const item of inputs) {
        const li = $('<li class="ml-1">');
        li.append(item.label, item.input);
        list.append(li);
    }
}
