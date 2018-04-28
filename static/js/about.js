$( document ).ready(function () {
    $("#sidenav").sideNav();

    $(".dropdown-button").dropdown();
    $('.dropdown-button').dropdown({
        hover: true, // Activate on hover
        belowOrigin: true, // Displays dropdown below the button
        alignment: 'left', // Displays dropdown with edge aligned to the left of button
    });

    load_team_members();
});

function load_team_members() {
    for (var i = 0; i < team.length; i++) {
        member = team[i];
        var container = document.createElement('div');
        container.className = "member-container col s12 m4";

        var image = document.createElement('img');
        image.src = "/static/img/team/" + member.image;
        image.className = "circle responsive-img member-image";

        container.appendChild(image);

        var name = document.createElement('div');
        name.className = "member-name";
        name.innerText = member.name;

        container.appendChild(name);

        var department = document.createElement('div');
        department.className = "member-department";
        department.innerText = member.department;
        department.setAttribute('style', 'text-align:center');

        container.appendChild(department);

        $('#team-container').append(container);
        console.log(container)
    }
}
