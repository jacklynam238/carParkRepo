let dateInputs = document.getElementsByClassName('date');
let timesInputs = document.getElementsByClassName('times');
let spotInputs = document.getElementsByClassName('spot');

let idInputs = document.getElementsByClassName('bookingId');
let forms = document.getElementsByTagName('form');

let buttonContainer = document.getElementsByClassName('buttonContainer');
let originalButtonsHTML =  "";
let updatingButtonsHTML =  `<div class="row buttonContainer">
                                <button style="margin-left: auto;" class="delete" onClick="cancelChanges(1)">Cancel</button>
                                <button style="width: auto;" class="update" onClick="applyChanges(1)">Apply</button>
                            </div>`;

let dateValue, endTimeValue, startTimeValue, spotValue = 0;

function updateBooking(bookingIndex) {
    dateValue = dateInputs[bookingIndex-1].innerHTML;
    endTimeValue = timesInputs[bookingIndex-1].innerHTML.slice(15, 20);
    startTimeValue = timesInputs[bookingIndex-1].innerHTML.slice(0, 5);
    spotValue = spotInputs[bookingIndex-1].innerHTML;

    dateInputs[bookingIndex-1].innerHTML = "<input name='date' value='" + dateValue + "' type='date'/>";
    timesInputs[bookingIndex-1].innerHTML = "<input name='startTime' value='" + startTimeValue + "' type='time'/> until <input name='endTime' value='" + endTimeValue + "' type='time'/>";
    spotInputs[bookingIndex-1].innerHTML = "<input name='spot' value='" + spotValue + "' type='number'/>";

    originalButtonsHTML =  buttonContainer[bookingIndex-1].innerHTML;
    let updatingButtonsHTML =  `<div class="row buttonContainer">
                                    <button style="margin-left: auto;" class="delete" onClick="cancelChanges(${bookingIndex})">Cancel</button>
                                    <button style="width: auto;" class="update" onClick="applyChanges(${bookingIndex})">Apply</button>
                                </div>`;
    buttonContainer[bookingIndex-1].innerHTML = updatingButtonsHTML;
}

function cancelChanges(bookingIndex) {
    buttonContainer[bookingIndex-1].innerHTML = originalButtonsHTML;
    dateInputs[bookingIndex-1].innerHTML = dateValue;
    timesInputs[bookingIndex-1].innerHTML = startTimeValue + ":00 until " + endTimeValue + ":00";
    spotInputs[bookingIndex-1].innerHTML = spotValue;
}

function applyChanges(bookingIndex) {
    forms[bookingIndex-1].submit();
}