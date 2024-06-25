if (error == 1) {errorMessage = "No account is registered with that email";}

errorHTML = `<div class="error">
                    <h2>Error:</h2>
                    <p>` + errorMessage + `</p>
                </div>`;
errorContainer = document.getElementById("errorContainer");
errorContainer.innerHTML = errorHTML;