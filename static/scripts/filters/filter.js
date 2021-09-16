import { loadUsersFilter } from "./users.js";

const script = $('script[src$="filter.js"]');
const endpoint = script.attr('data-endpoint');
const filterList = $('#filter_items');

$(document).ready(() => {
    
    switch (endpoint) {
        case 'users':
            const noFilters = $('#no-filters');
            noFilters.css('display', 'none')
            loadUsersFilter(filterList);
            break;

        default:
            break;
    }
});
