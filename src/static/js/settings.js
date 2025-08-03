function changeDefaultHourly() {
    const newHourly = document.getElementById("newHourly").value;

    fetch("changeDefaultHourly", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            newHourly: newHourly,
        })
    }).then((response) => {
        if (!response.ok) {
            response.json().then((json) => {
                alert("Error: " + response.status + ", " + json["status"]);
            })
            return;
        }

        window.location.reload();
        return;
    })
}