$( document ).ready(function () {
    $("#sidenav").sideNav();

    $(".dropdown-button").dropdown();
    $('.dropdown-button').dropdown({
        hover: true, // Activate on hover
        belowOrigin: true, // Displays dropdown below the button
        alignment: 'left', // Displays dropdown with edge aligned to the left of button
    });

    load_unregistered_table();
    load_registered_table();
});

function load_unregistered_table() {
    var arr = ['Name', 'Email ID', 'RFID Number'];
    for(var i = 0; i < arr.length; i++) {
        var grid = document.createElement('h3');
        grid.className = "users-not-approved-grid-item flow-text";
        grid.setAttribute('id', arr[i]);
        grid.innerText = arr[i];
        $('#users_not_approved').append(grid);
    }
    load_users('no_rfid_number');

}

function load_registered_table() {
    var arr = ['Name', 'Email ID', 'RFID Number']
    for(var i = 0; i < arr.length; i++) {
        var grid = document.createElement('h3');
        grid.className = "users-approved-grid-item flow-text";
        grid.setAttribute('id', arr[i]);
        grid.innerText = arr[i];
        $('#users_approved').append(grid);
    }
    load_users('rfid_number');

}


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
    });
}

function load_unregistered_users(text) {
    console.log(text);
    text = JSON.parse(text);
    for (var i = 0; i < text.length; i ++) {

        // document.write(text);
        user_detail = text[i]
        // Name -> 1, Email ID  -> 2, RFID Number -> 4
        var arr = [1, 2, 4]

        for (var j = 0; j < arr.length; j ++) {
            var grid = document.createElement('div');
            if (user_detail[arr[j]] == '' || user_detail[arr[j]] == null) {
                user_detail[arr[j]] = '<i class="small material-icons">create</i>';
                grid.onclick('')
            }
            grid.className = "users-not-approved-grid-item flow-text";
            // grid.setAttribute('id', j);
            grid.innerHTML = user_detail[arr[j]];
            $('#users_not_approved').append(grid);
        }
    }
}

function load_registered_users(text) {
    console.log(text);
    text = JSON.parse(text);
    for (var i = 0; i < text.length; i ++) {

        // document.write(text);
        user_detail = text[i]
        // Name -> 1, Email ID  -> 2, RFID Number -> 4
        var arr = [1, 2, 4]

        for (var j = 0; j < arr.length; j ++) {
            if (user_detail[arr[j]] == '') {
                user_detail[arr[j]] = 'None'
            }
            var grid = document.createElement('div');
            grid.className = "users-approved-grid-item flow-text";
            grid.setAttribute('id', user_detail[arr[j]]);
            grid.innerText = user_detail[arr[j]];
            $('#users_approved').append(grid);
        }
    }
}