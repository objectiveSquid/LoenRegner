function signup() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch("/createAccount", {
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
            alert("Error: " + response.status);
            return;
        }

        response.text().then((uuid) => {
            if (uuid === null) {
                alert("Error: " + response.status);
                return;
            }
            
            fetch("/getSessionID", {
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
                    alert("Error: " + response.status);
                    return;
                }
                
                response.text().then((text) => {
                    document.cookie = "SessionID=" + text;
                    window.location.href = "/shifts";
                })
            })
        })
    })
};

