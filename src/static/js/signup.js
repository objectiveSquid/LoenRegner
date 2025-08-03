function signup() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const hourly = document.getElementById("hourly").value;

    fetch("createAccount", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password,
            hourly: hourly,
        })
    }).then((response) => {
        if (!response.ok) {
            response.json().then((json) => {
                alert("Error: " + response.status + ", " + json["status"]);
            })
            return;
        }

        response.text().then((uuid) => {
            if (uuid === null) {
                response.json().then((json) => {
                    alert("Error: " + response.status + ", " + json["status"]);
                })
                return;
            }
            
            fetch("getSessionID", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            }).then((response) => {
                if (!response.ok) {
                    response.json().then((json) => {
                        alert("Error: " + response.status + ", " + json["status"]);
                    })
                    return;
                }
                
                response.text().then((text) => {
                    document.cookie = "SessionID=" + text;
                    window.location.href = "shifts";
                })
            })
        })
    })
};

