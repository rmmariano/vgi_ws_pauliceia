$(document).ready(function(){

    function login(args) {
        args._xsrf = get_tornado_cookie("_xsrf");

        var request = $.ajax({
            url: "/auth/login/",
            method: "POST",
            data: $.param(args),
            dataType: "text",
        });

        request.done(function(data, textStatus, information) {
            console.log("done :D ");

            // convert string into JSON
            data = $.parseJSON(data);

            console.log(data);
        });

        request.fail(function(data, textStatus, information) {
            console.log("fail x( ");

            // get the important information
            data = get_important_data(data);

            console.log(data);
        });

    };

    $('#login_form').submit(function(ev) {
        // to stop the form from default submitting
        ev.preventDefault();

        var type_login = $('#type_login input:radio:checked').val();

        var args = {
                "email": $("#email").val(),
                "password": $("#password").val(),
                "type_login": type_login,
            };

        login(args);
    });

});
