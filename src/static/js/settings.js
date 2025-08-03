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
                alert("Fejl: " + response.status + ", " + json["status"]);
            })
            return;
        }

        window.location.reload();
        return;
    })
}

function changeTaxStart() {
    const newTaxStart = document.getElementById("newTaxStart").value;

    fetch("changeTaxStart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            newTaxStart: newTaxStart,
        })
    }).then((response) => {
        if (!response.ok) {
            response.json().then((json) => {
                alert("Fejl: " + response.status + ", " + json["status"]);
            })
            return;
        }

        window.location.reload();
        return;
    })
}