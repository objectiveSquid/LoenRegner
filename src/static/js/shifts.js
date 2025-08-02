function addShift() {
    const starttime = document.getElementById("starttime").value;
    const stoptime = document.getElementById("stoptime").value;
    const hourly = document.getElementById("hourly").value;

    fetch("/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            starttime: starttime,
            stoptime: stoptime,
            hourly: hourly,
        })
    }).then((response) => {
        if (!response.ok) {
            alert("Error: " + response.status);
            return;
        }

        window.location.href = "/shifts";
    });
}