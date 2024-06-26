// error message
if (error == 1) {errorMessage = "That email is invalid";}

// add error to html
errorHTML = `<div class="error">
                    <h2>Error:</h2>
                    <p>` + errorMessage + `</p>
                </div>`;
errorContainer = document.getElementById("errorContainer");
errorContainer.innerHTML = errorHTML;