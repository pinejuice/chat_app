$(function() {
    $(".submenu").click(function () {
        const submenu_class = document.getElementById('submenu');
        const submenu_info = document.getElementById('submenu_info');
        if(submenu_class.classList.contains('open') === true) {
            submenu_class.classList.remove('open');
            submenu_info.style.display = 'none';
        } else {
            submenu_class.classList.add('open');
            submenu_info.style.display = '';
        }
    });
    $(".user_list_top").click(function () {
        const user_list = document.getElementById('user_list');
        const user_list_top = document.getElementById('user_list_top');
        if(user_list_top.classList.contains('open') === true) {
            user_list_top.classList.remove('open');
            user_list.style.display = 'none'
        } else {
            user_list_top.classList.add('open');
            user_list.style.display = ''
        }
    });
});