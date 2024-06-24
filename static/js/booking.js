const seats = document.querySelectorAll('.seat');
const selectedSpotDisplay = document.getElementById('selectedSpot');
const input = document.getElementById('parkSpot');

seats.forEach(seat => {
    seat.addEventListener('click', () => {
        if(!seat.classList.contains('unavailable')) {
            seats.forEach(s => s.classList.remove('selected'));
            seat.classList.add('selected');
            input.value = seat.dataset.seat;
        }
    });
});

const dateInput = document.getElementById('date');
const startTimeInput = document.getElementById('time');
const endTimeInput = document.getElementById('endTime');

dateInput.addEventListener('input', updateAvailableSeats);
startTimeInput.addEventListener('input', updateAvailableSeats);
endTimeInput.addEventListener('input', updateAvailableSeats);

function updateAvailableSeats() {
    let data = new FormData();
    data.append("date", dateInput.value);
    data.append("startTime", startTimeInput.value);
    data.append("endTime", endTimeInput.value);

    fetch(requestUrl, {
        "method": "POST",
        "body": data,
    }).then(response => response.json()).then(json => {
        seats.forEach(s => s.classList.remove('unavailable'));
        for (let i=0; i<json.length; i++) {
            seats[json[i] - 1].classList.add('unavailable');
            if (seats[json[i] - 1].classList.contains('selected')) {
                seats[json[i] - 1].classList.remove('selected');
                input.value = 0;
            }
        }
        console.log(json);
    })
}

if (error == 1) {errorMessage = "No parking spot chosen";}
if (error == 2) {errorMessage = "You must be logged in to make a booking";}
if (error == 3) {errorMessage = "Start time must be within opening hours (7:00AM - 7:00PM)";}
if (error == 4) {errorMessage = "End time must be within opening hours (7:00AM - 7:00PM)";}
if (error == 5) {errorMessage = "Start time must come before end time";}
if (error == 6) {errorMessage = "Bookings cannot be longer than 3 hours";}
if (error == 7) {errorMessage = "Bookings cannot be shorter than 30 minutes";}
if (error == 8) {errorMessage = "Bookings cannot be made in the past";}


errorHTML = `<div class="error">
                    <h2>Error:</h2>
                    <p>` + errorMessage + `</p>
                </div>`;
errorContainer = document.getElementById("errorContainer");
errorContainer.innerHTML = errorHTML;