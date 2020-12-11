$('#input_user_icon').on('change', function (e) {
    var reader = new FileReader();
    reader.onload = function (e) {
        $("#user_info_icon").attr('src', e.target.result);
    }
    reader.readAsDataURL(e.target.files[0]);
});