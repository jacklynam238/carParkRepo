navigation = document.getElementById('navigation');

if (userId == 0) {
    userLoggedOut();
} else {
    userLoggedIn();
}

function userLoggedOut() {
    let insertHTML = `
        <li><a class="active" href="/"><img src="../static/images/ericsson text logo.png" alt="Logo" class="logo"></a></li>
        <li style="float:right"><a class="active" href="/signup">Sign-up</a></li>
        <li style="float:right"><a class="active" href="/login">Log-in</a></li>
        <li style="float:right"><a class="active" href="/about">About</a></li>
        <li style="float:right"><a class="active" href="/contact">Contact</a></li>
        <li style="float:right"><a class="active" href="/booking">Book Now</a></li>
    `;
    navigation.innerHTML = insertHTML;
}

function userLoggedIn() {
    let insertHTML = `
        <li><a class="active" href="/"><img src="../static/images/ericsson text logo.png" alt="Logo" class="logo"></a></li>
        <li style="float:right"><a class="active" href="/logout">Log-out</a></li>
        <li style="float:right"><a class="active" href="/about">About</a></li>
        <li style="float:right"><a class="active" href="/contact">Contact</a></li>
        <li style="float:right"><a class="active" href="/booking">Book Now</a></li>
    `;
    navigation.innerHTML = insertHTML;
}