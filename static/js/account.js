// <p> tags containing booking info
let dateInputs = document.getElementsByClassName('date');
let timesInputs = document.getElementsByClassName('times');
let spotInputs = document.getElementsByClassName('spot');
// find booking ids
let idInputs = document.getElementsByClassName('bookingId');
let forms = document.getElementsByTagName('form');
// booking buttons
let buttonContainer = document.getElementsByClassName('buttonContainer');
let originalButtonsHTML =  "";
let updatingButtonsHTML =  `<div class="row buttonContainer">
                                <button style="margin-left: auto;" class="delete" onClick="cancelChanges(1)">Cancel</button>
                                <button style="width: auto;" class="update" onClick="applyChanges(1)">Apply</button>
                            </div>`;

let dateValue, endTimeValue, startTimeValue, spotValue = 0;

function updateBooking(bookingIndex) {
    // store booking info
    dateValue = dateInputs[bookingIndex-1].innerHTML;
    endTimeValue = timesInputs[bookingIndex-1].innerHTML.slice(15, 20);
    startTimeValue = timesInputs[bookingIndex-1].innerHTML.slice(0, 5);
    spotValue = spotInputs[bookingIndex-1].innerHTML;

    // convert booking info sections to input tags
    dateInputs[bookingIndex-1].innerHTML = "<input name='date' value='" + dateValue + "' type='date'/>";
    timesInputs[bookingIndex-1].innerHTML = "<input name='startTime' value='" + startTimeValue + "' type='time'/> until <input name='endTime' value='" + endTimeValue + "' type='time'/>";
    spotInputs[bookingIndex-1].innerHTML = "<input name='spot' value='" + spotValue + "' type='number'/>";

    // change buttons to apply and cancel buttons
    originalButtonsHTML =  buttonContainer[bookingIndex-1].innerHTML;
    let updatingButtonsHTML =  `
                                    <button style="margin-left: auto;" class="delete" onClick="cancelChanges(${bookingIndex})">Cancel</button>
                                    <button style="width: auto;" class="update" onClick="applyChanges(${bookingIndex})">Apply</button>
                               `;
    buttonContainer[bookingIndex-1].innerHTML = updatingButtonsHTML;
}

function cancelChanges(bookingIndex) {
    // revert input tags back to <p> tags with stored data
    buttonContainer[bookingIndex-1].innerHTML = originalButtonsHTML;
    dateInputs[bookingIndex-1].innerHTML = dateValue;
    timesInputs[bookingIndex-1].innerHTML = startTimeValue + ":00 until " + endTimeValue + ":00";
    spotInputs[bookingIndex-1].innerHTML = spotValue;
}

function applyChanges(bookingIndex) {
    /* submit form to flask */
    forms[bookingIndex-1].submit();
}

// error messages
if (error == 1) {errorMessage = "Invalid form data. Please make sure all fields are filled out";}
if (error == 2) {errorMessage = "Start time must be within opening hours (7:00AM - 7:00PM)";}
if (error == 3) {errorMessage = "End time must be within opening hours (7:00AM - 7:00PM)";}
if (error == 4) {errorMessage = "Start time must come before end time";}
if (error == 5) {errorMessage = "Bookings cannot be longer than 3 hours";}
if (error == 6) {errorMessage = "Bookings cannot be shorter than 30 minutes";}
if (error == 7) {errorMessage = "Bookings cannot be made in the past";}
if (error == 8) {errorMessage = "Booking clashes with another. Please select a different parking spot or time and try again.";}

// add error message to page
// add error message to page
errorHTML = `<div class="error">
                    <h2>Error:</h2>
                    <p>` + errorMessage + `</p>
                </div>`;
errorContainer = document.getElementById("errorContainer");
errorContainer.innerHTML = errorHTML;