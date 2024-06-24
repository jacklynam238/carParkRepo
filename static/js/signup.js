if (error == 1) {errorMessage = "Passwords don't match";}
if (error == 2) {errorMessage = "Email Already associated with another account";}
if (error == 3) {errorMessage = "Email is invalid";}
if (error == 4) {errorMessage = "Password needs to have a min of 10 characters";}
if (error == 5) {errorMessage = "Password needs an uppercase letter";}
if (error == 6) {errorMessage = "Password needs a number";}
errorHTML = `<div class="error">
                    <h2>Error:</h2>
                    <p>` + errorMessage + `</p>
                </div>`;
errorContainer = document.getElementById("errorContainer");
errorContainer.innerHTML = errorHTML;