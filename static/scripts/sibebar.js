function closeAll() {
    const allLists = $('.sidebar-container div[id$="_list"]');
    allLists.css('display', 'none');
}

const buttons = $('.sidebar-container img[id$="_button"]');

buttons.click((e) => {
    const list = $(`.sidebar-container div[id="${e.target.id.split('_')[0]}_list"]`);
    const display = list[0].style['display'];
    closeAll();

    if (display === 'none') list.css('display', 'flex');
    else list.css('display', 'none');
});
