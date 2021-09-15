/**
 * Event Handler for radio buttons when filtering users
 * @param {String} filter_value String value of a users chosen role 
 * Ex. 'Front-End' or 'both'
 */
function handleOnChange(filter_value) {
    const users = $('section div.user-card');
    
    for (const user of users) {
        user.style.display = 'none';
        const userRoles = user.getAttribute('data-role').split(':');  // ex. 'Front-End:Back-End' => ['Front-End', 'Back-End']

        if (filter_value === 'all') {
            user.style.display = 'block';
            continue;
        }

        if (filter_value === 'both') {
            const hasBothRoles = (userRoles.includes('Front-End') && userRoles.includes('Back-End'));
            if (hasBothRoles) user.style.display = 'block';
            continue;
        }

        for (const role of userRoles) {
            if (filter_value === role) {
                user.style.display = 'block';
                break;
            }
        }
    }
}

/**
 * Create & Load list Elements as user filter options to the page
 * @param {HTMLUListElement} list Destination UL element to hold list items
 */
export function loadUsersFilter(list) {
    // Create radio buttons
    const showAll = {
        label: $('<label class="m-0 col-6 p-0" for="rb_show_all">Show All</label>'),
        input: $('<input class="ml-1 filter_item" type="radio" name="role" id="rb_show_all" value="all" checked />')
    };

    const showFrontEnd = {
        label: $(`<label class="m-0 col-6 p-0" for="rb_Front-End">Front-End</label>`),
        input: $(`<input class="ml-1 filter_item" type="radio" name="role" id="rb_Front-End" value="Front-End" />`)
    };

    const showBackEnd = {
        label: $(`<label class="m-0 col-6 p-0" for="rb_Back-End">Back-End</label>`),
        input: $(`<input class="ml-1 filter_item" type="radio" name="role" id="rb_Back-End" value="Back-End" />`)
    };

    const showBoth = {
        label: $('<label class="m-0 col-6 p-0" for="rb_show_both">Both</label>'),
        input: $('<input class="ml-1 filter_item" type="radio" name="role" id="rb_show_both" value="both" />')
    };

    // Add Event Handlers to radio buttons
    showAll.input.change(() => { handleOnChange('all') });
    showFrontEnd.input.change(() => { handleOnChange('Front-End') });
    showBackEnd.input.change(() => { handleOnChange('Back-End') });
    showBoth.input.change(() => { handleOnChange('both') });

    // Add list items to DOM
    const inputs = [ showAll, showFrontEnd, showBackEnd, showBoth ];

    for (const item of inputs) {
        const li = $('<li class="ml-1 mb-1 row align-items-center">');
        li.append(item.label, item.input);
        list.append(li);
    }
}
