// error message
if (error == 1) {errorMessage = "No account is registered with that email";}
if (error == 2) {errorMessage = "Incorrect Password";}
if (error == 3) {errorMessage = "Failed to connect to database";}

// add error to html
errorHTML = `<div class="error">
                    <h2>Error:</h2>
                    <p>` + errorMessage + `</p>
                </div>`;
errorContainer = document.getElementById("errorContainer");
errorContainer.innerHTML = errorHTML;