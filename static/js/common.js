//
// Responsible file to do some issues dynamically that is common for all JS files
//

function get_important_data(data){
    return {
        "status": data["status"],
        "statusText": data["statusText"],
        "responseText": data["responseText"],
        "extra": "extra" in data ? data["extra"] : "",
    };
}

function get_tornado_cookie(name) {
    // http://www.tornadoweb.org/en/stable/guide/security.html
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}








// other functions

function require(script) {
    //
    // Responsible function to ...
    //
    // Args:
    //     Nothing until the moment
    //
    // Returns:
    //     Nothing until the moment
    //
    // Raises:
    //     Nothing until the moment
    //

    // require("/static/not_own/FileSaver/FileSaver.js");

    $.ajax({
        url: script,
        dataType: "script",
        async: false,           // <-- This is the key
        success: function () {
            // all good...
        },
        error: function () {
            throw new Error("Could not load script " + script);
        }
    });
}


String.prototype.capitalizeFirstLetter = function() {
    //
    // Responsible function to ...
    //
    // Args:
    //     Nothing until the moment
    //
    // Returns:
    //     Nothing until the moment
    //
    // Raises:
    //     Nothing until the moment
    //

    // Insert the function capitalizeFirstLetter for all strings existents
    return this.charAt(0).toUpperCase() + this.slice(1);
}

String.prototype.replaceAt = function(index, char) {
    var a = this.split("");
    a[index] = char;
    return a.join("");
}

String.prototype.isNumber = function (){
    // int
    if(this.match(/^\d+$/))
        return true;
    // float
    if(this.match(/^\d+\.\d+$/))
        return true;

    return false;
}

function isInteger(n){
    return Number(n) === n && n % 1 === 0;
}

function isFloat(n){
    return Number(n) === n && n % 1 !== 0;
}


function remove_underscore_and_capitalize_first_letter(word){
    //
    // Responsible function to ...
    //
    // Args:
    //     Nothing until the moment
    //
    // Returns:
    //     Nothing until the moment
    //
    // Raises:
    //     Nothing until the moment
    //

    // replace all ocurrences of "_" to " "
    return word.replace(/_/g, " ").capitalizeFirstLetter();
}


function export_file(text_to_export, name_file, id){
    //
    // Responsible function to ...
    //
    // Args:
    //     Nothing until the moment
    //
    // Returns:
    //     Nothing until the moment
    //
    // Raises:
    //     Nothing until the moment
    //

    var a_link = $("#" + id)[0];

    a_link.href = window.URL.createObjectURL(
        new Blob(
            [text_to_export],
            {type: 'text/plain;charset=utf-8;'}
        )
    );
    a_link.download = name_file;
}


function export_file_csv(text_to_export, name_file, id){
    //
    // Responsible function to ...
    //
    // Args:
    //     Nothing until the moment
    //
    // Returns:
    //     Nothing until the moment
    //
    // Raises:
    //     Nothing until the moment
    //

    var a_link = $("#" + id)[0];

    a_link.href = window.URL.createObjectURL(
        new Blob(
            [text_to_export],
            {type: "data:text/csv;charset=utf-8,"}
        )
    );
    a_link.download = name_file;
}


function get_formated_date(date){
    //
    // Responsible function to ...
    //
    // Args:
    //     Nothing until the moment
    //
    // Returns:
    //     Nothing until the moment
    //
    // Raises:
    //     Nothing until the moment
    //

    var day = date.slice(0,2),
        month = date.slice(2,4),
        year = date.slice(4,8);

    var new_date = new Date(month + "/" + day + "/" + year);

    var monthNames = ["jan.", "fev.", "mar.", "abr.", "mai.", "jun.", "jul.", "ago.", "set.", "out.", "nov.", "dez."];

    var day = new_date.getDate();
    var monthIndex = new_date.getMonth();
    var year = new_date.getFullYear();

    if(day < 10)
        day = '0' + day;

    formated_date = day + " " + monthNames[monthIndex] + " " + year;

    return formated_date;
}

function get_actual_date(){
    //
    // Responsible function to ...
    //
    // Args:
    //     Nothing until the moment
    //
    // Returns:
    //     Nothing until the moment
    //
    // Raises:
    //     Nothing until the moment
    //

    var today = new Date(),
        dd = today.getDate(),
        mm = today.getMonth() + 1, // January is 0
        yyyy = today.getFullYear();

    if(dd < 10)
        dd = '0' + dd;

    if(mm < 10)
        mm = '0' + mm;

    actual_date = dd + '/' + mm + '/' + yyyy;
    actual_hour = today.getHours() + "h" + today.getMinutes();

    return  {"actual_date": actual_date, "actual_hour": actual_hour};

}
