function deleteBooking() {
    fetch("http://backendurl/delete", {
        method: "DELETE",
        headers: {...}
        body: JSON.stringify({each.id}),
    });
}