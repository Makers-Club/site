

export function getElements() {
    const list = $('#notification_list');
    const button = $('#notification_button');
    const close = $('#notification_list_close');
    const container = $('#notifications');
    const iconExample = $('#icon');
    close.css('position', 'absolute');
    close.css('top', '.5rem');
    close.css('right', '.5rem');
 
    return { list, button, close, container, iconExample };
}


