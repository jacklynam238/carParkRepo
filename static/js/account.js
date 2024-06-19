let dateInputs = document.getElementsByClassName('date');
let timesInputs = document.getElementsByClassName('times');
let spotInputs = document.getElementsByClassName('spot');

let buttonContainer = document.getElementsByClassName('');
let updateButton = buttonContainer.getElementsByClassName('')[0];
let deleteButton = buttonContainer.getElementsByClassName('')[0];

let completeButtonHTML = "";
let cancelButtonHTML = "";

function updateBooking(bookingIndex) {
    let dateValue = dateInputs[bookingIndex-1].innerHTML;
    let endTimeValue = timesInputs[bookingIndex-1].innerHTML.slice(15);
    let startTimeValue = timesInputs[bookingIndex-1].innerHTML.slice(0, 8);
    let spotValue = spotInputs[bookingIndex-1].innerHTML;

    dateInputs[bookingIndex-1].innerHTML = "<input name='date' value='" + dateValue + "' type='date'/>";
    timesInputs[bookingIndex-1].innerHTML = "<input name='startTime' value='" + startTimeValue + "' type='time'/> until <input name='endTime' value='" + endTimeValue + "' type='time'/>";
    spotInputs[bookingIndex-1].innerHTML = "<input name='spot' value='" + spotValue + "' type='number'/>";
}