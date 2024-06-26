// image carousel
let slideIndex = 0;
showSlides();

function showSlides() {
    // DOM variables
    let i;
    let slides = document.getElementsByClassName("mySlides");

    // hide slides
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }

    // change slide
    slideIndex++;

    // loop slides
    if (slideIndex > slides.length) {slideIndex = 1}

    // show slide
    slides[slideIndex-1].style.display = "block";
    setTimeout(showSlides, 2000); // Change image every 2 seconds
}