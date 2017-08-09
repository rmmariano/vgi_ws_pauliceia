$(document).ready(function(){

    $.ajax({
        url: 'http://localhost:8888/get/point/tb_places/see',
        dataType: 'application/json',
        complete: function(data){
            console.log("complete");
            console.log(data["responseText"]);
            console.log(data);
        },
        success: function(data){
            console.log("success");
            console.log(data["responseText"]);
            console.log(data);
        }
    });

//    $.ajax({
//        url: 'http://headers.jsontest.com/?mime=1',
//        dataType: 'application/json',
//        complete: function(data){
//            console.log("complete");
//            console.log(data["responseText"]);
//            console.log(data);
//        },
//        success: function(data){
//            console.log("success");
//            console.log(data["responseText"]);
//            console.log(data);
//        }
//    });
//
//    $.ajax({
//        url: 'https://api.twitter.com/1.1/statuses/user_timeline.json',
//        dataType: 'application/json',
//        complete: function(data){
//            console.log("complete");
//            console.log(data["responseText"]);
//            console.log(data);
//        },
//        success: function(data){
//            console.log("success");
//            console.log(data["responseText"]);
//            console.log(data);
//        }
//    });

});
