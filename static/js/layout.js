$(function() {
    $(".submenu").click(function () {
        const submenu_class = document.getElementById('submenu');
        const submenu_info = document.getElementById('submenu_info')
        if(submenu_class.classList.contains('open') === true) {
            submenu_class.classList.remove('open')
            submenu_info.style.display = 'none';
        } else {
            submenu_class.classList.add('open');
            submenu_info.style.display = '';
        }
    });
});