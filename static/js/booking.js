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

