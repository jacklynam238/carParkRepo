// get nav container
navigation = document.getElementById('navigation');

if (userId == 0) {          //user logged out
    userLoggedOut();
} else if (userId == 1) {   //admin logged in
    adminLoggedIn();
} else {                    //user logged in
    userLoggedIn();
}

function userLoggedOut() {
    let insertHTML = `
        <li><a class="active" href="/"><img src="../static/images/ericsson text logo.png" alt="Logo" class="logo"></a></li>
        <li style="float:right"><a class="active" href="/signup">Sign-up</a></li>
        <li style="float:right"><a class="active" href="/login">Log-in</a></li>
        <li style="float:right"><a class="active" href="/about">About</a></li>
        <li style="float:right"><a class="active" href="/contact/0">Contact</a></li>
        <li style="float:right"><a class="active" href="/booking/0">Book Now</a></li>
    `;
    navigation.innerHTML = insertHTML;
}

function userLoggedIn() {
    let insertHTML = `
        <li><a class="active" href="/"><img src="../static/images/ericsson text logo.png" alt="Logo" class="logo"></a></li>
        <li style="float:right"><a class="active" href="/account/0">My Account</a></li>
        <li style="float:right"><a class="active" href="/about">About</a></li>
        <li style="float:right"><a class="active" href="/contact/0">Contact</a></li>
        <li style="float:right"><a class="active" href="/booking/0">Book Now</a></li>
    `;
    navigation.innerHTML = insertHTML;
}

function adminLoggedIn() {
    let insertHTML = `
        <li><a class="active" href="/"><img src="../static/images/ericsson text logo.png" alt="Logo" class="logo"></a></li>
        <li style="float:right"><a class="active" href="/admin">Admin</a></li>
        <li style="float:right"><a class="active" href="/about">About</a></li>
        <li style="float:right"><a class="active" href="/contact/0">Contact</a></li>
        <li style="float:right"><a class="active" href="/booking/0">Book Now</a></li>
    `;
    navigation.innerHTML = insertHTML;
}