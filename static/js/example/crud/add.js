$(document).ready(function(){

    $('#not_found_path').click(function(){

        var points_to_add = [
            {
                "id_user": 6,
                "description": null,
                "id_street": 22,
                "geom": "POINT(-5191508.6860944 -2698228.13572069)",
                "first_day": null
            }
        ];


        var request = $.ajax({
            url: "/add/geometry/",
            method: "POST",
            data: JSON.stringify(points_to_add),
            contentType: "application/json"
        });

        request.done(function(data, textStatus, information) {
            console.log("done :D ");

            // convert string into JSON
            data = $.parseJSON(data);

            console.log(data);
        });

        request.fail(function(data, textStatus, information) {
            console.log("fail x( ");
            console.log(data["statusText"]);
            console.log(data);
        });

//        request.always(function(data, textStatus, information) {
//            console.log("always x) ");
//            console.log(data);
//        });

    });


    $('#insert_one_point').click(function(){

        var points_to_add = [
            {
                "id_user": 6,
                "description": null,
                "last_day": null,
                "last_year": null,
                "first_month": null,
                "source": "Almanak Laemmert, 1931, v.II, p. 96",
                "original_number": null,
                "last_month": null,
                "name": "TEST_1",
                "number": 34,
                "id_street": 22,
                "geom": "POINT(-5191508.6860944 -2698228.13572069)",
                "first_year": 1931,
                "id": 45,
                "date": "2017-08-01",
                "first_day": null
            }
        ];


        var request = $.ajax({
            url: "/add/geometry/tb_places",
            method: "POST",
            data: JSON.stringify(points_to_add),
            contentType: "application/json"
        });

        request.done(function(data, textStatus, information) {
            console.log("done :D ");

            // convert string into JSON
            data = $.parseJSON(data);

            console.log(data);
        });

        request.fail(function(data, textStatus, information) {
            console.log("fail x( ");
            console.log(data["statusText"]);
            console.log(data);
        });

//        request.always(function(data, textStatus, information) {
//            console.log("always x) ");
//            console.log(data);
//        });

    });


    $('#insert_one_point_in_geojson').click(function(){

        var points_to_add = [
            {
                "id_user": 6,
                "description": null,
                "last_day": null,
                "last_year": null,
                "first_month": null,
                "source": "Almanak Laemmert, 1931, v.II, p. 96",
                "original_number": null,
                "last_month": null,
                "name": "TEST_1",
                "number": 34,
                "id_street": 22,
                "geom": {
                  "type": "Point",
                  "coordinates": [ -5191508.6860944, -2698228.13572069 ]
                },
                "first_year": 1931,
                "id": 45,
                "date": "2017-08-01",
                "first_day": null
            }
        ];

        var request = $.ajax({
            url: "/add/geometry/tb_places/?geom_format=geojson",
            method: "POST",
            data: JSON.stringify(points_to_add),
            contentType: "application/json"
        });

        request.done(function(data, textStatus, information) {
            console.log("done :D ");

            // convert string into JSON
            data = $.parseJSON(data);

            console.log(data);
        });

        request.fail(function(data, textStatus, information) {
            console.log("fail x( ");
            console.log(data["statusText"]);
            console.log(data);
        });

//        request.always(function(data, textStatus, information) {
//            console.log("always x) ");
//            console.log(data);
//        });

    });


    $('#insert_one_point_with_tags').click(function(){

        var points_to_add = [
            {
                "id_user": 6,
                "description": null,
                "last_day": null,
                "last_year": null,
                "first_month": null,
                "source": "Almanak Laemmert, 1931, v.II, p. 96",
                "original_number": null,
                "last_month": null,
                "name": "TEST_1",
                "number": 34,
                "id_street": 22,
                "geom": "POINT(-5191508.6860944 -2698228.13572069)",
                "first_year": 1931,
                "id": 45,
                "date": "2017-08-01",
                "first_day": null,
                "tags": [
                    {"k": "link", "v": "https://name.site/artigo.pdf"},
                    {"k": "link", "v": "https://name.site/tese.pdf"},
                ]
            }
        ];


        var request = $.ajax({
//            url: "/add/geometry/tb_places",
            url: "http://localhost:8888/add/geometry/tb_places",
            method: "POST",
            data: JSON.stringify(points_to_add),
            contentType: "application/json"
        });

        request.done(function(data, textStatus, information) {
            console.log("done :D ");

            // convert string into JSON
            data = $.parseJSON(data);

            console.log(data);
        });

        request.fail(function(data, textStatus, information) {
            console.log("fail x( ");
            console.log(data["statusText"]);
            console.log(data);
        });

//        request.always(function(data, textStatus, information) {
//            console.log("always x) ");
//            console.log(data);
//        });

    });

});
