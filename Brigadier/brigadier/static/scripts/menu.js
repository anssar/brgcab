function drop() {
    var menu = document.getElementById('menu');
    if (!menu.dataset) {
        if (menu.getAttribute('data-expand') == 'false') {
            menu.className = 'menu menu-visible';
            menu.setAttribute('data-expand', 'true');
        } else {
            menu.className = 'menu';
            menu.setAttribute('data-expand', 'false');
        }
    }
    else {
        if (menu.dataset['expand'] == 'false') {
            menu.classList.add('menu-visible');
            menu.dataset['expand'] = 'true';
        } else {
            menu.classList.remove('menu-visible');
            menu.dataset['expand'] = 'false';
        }
    }
}