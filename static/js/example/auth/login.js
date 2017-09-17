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

            if(data["status"] == 200)  // 200 - OK
                // similar behavior as an HTTP redirect (don't back) (https://stackoverflow.com/questions/503093/how-to-redirect-to-another-webpage)
                window.location.replace("/auth/login/success/");

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

        var args = {
                "email": $("#email").val(),
                "password": sha512($("#password").val()),  // hash the password
            };

        login(args);
    });

});
