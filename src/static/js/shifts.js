function addShift() {
    const date = document.getElementById("date").value;
    const starttime = document.getElementById("starttime").value;
    const stoptime = document.getElementById("stoptime").value;
    const hourly = document.getElementById("hourly").value;

    fetch("add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            date: date,
            starttime: starttime,
            stoptime: stoptime,
            hourly: hourly,
        })
    }).then((response) => {
        if (!response.ok) {
            response.json().then((json) => {
                alert("Error: " + response.status + ", " + json["status"]);
            })
            return;
        }

        window.location.reload();
    });
}

function deleteShift(uuid) {
    fetch("delete", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            uuid: uuid,
        })
    }).then((response) => {
        if (!response.ok) {
            response.json().then((json) => {
                alert("Error: " + response.status + ", " + json["status"]);
            })
            return;
        }
        
        window.location.reload();
    });
}
