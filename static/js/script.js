$( document ).ready(function () {
    $("#sidenav").sideNav();

    $(".dropdown-button").dropdown();
    $('.dropdown-button').dropdown({
        hover: true, // Activate on hover
        belowOrigin: true, // Displays dropdown below the button
        alignment: 'left', // Displays dropdown with edge aligned to the left of button
    });

    load_users('no_rfid_number');
    load_users('rfid_number');

});

function load_users(rfid_status) {
    var response = '';
    $.ajax({
        url: '/load_users',
        data: JSON.stringify({ 'data': rfid_status}),
        contentType: 'application/json;charset=UTF-8',
        type: 'POST',
        success : function(text)
         {
             if(rfid_status == 'no_rfid_number') {
                 load_unregistered_users(text);
             }
             else {
                 load_registered_users(text);
             }
         },
        error: function (error) {
            console.log(error);
        }
    }).responseText;
}

function load_unregistered_users(text) {
    console.log(text);
    text = JSON.parse(text);
    for (var i = 0; i < text.length; i ++) {

        // document.write(text);
        user_detail = text[i].toString().split(',')
        for (var j = 0; j < user_detail.length; j ++) {
            if (user_detail[j] == '') {
                document.write('Empty');
            }
            else {
                document.write(user_detail[j]);
            }
            document.write("|");
        }
        document.write("\n|||");
    }
}

function load_registered_users(text) {
    // document.write(text);
}