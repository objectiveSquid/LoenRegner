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
                alert("Fejl: " + response.status + ", " + json["status"]);
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
                alert("Fejl: " + response.status + ", " + json["status"]);
            })
            return;
        }
        
        window.location.reload();
    });
}

function downloadShifts() {
    const raw = document.getElementById("downloadRawShifts").checked;

    window.open(`downloadShifts?raw=${raw}`, "_blank").focus();
}

function changeAMExceptionValue() {
    const value = document.getElementById("AMExceptionValue").checked;

    fetch("changeAMExceptionValue", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            value: value,
        })
    }).then((response) => {
        if (!response.ok) {
            response.json().then((json) => {
                alert("Fejl: " + response.status + ", " + json["status"]);
            })
            return;
        }

        window.location.reload();
    });
}
