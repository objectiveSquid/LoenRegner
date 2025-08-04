function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const rememberMe = document.getElementById("rememberMe").checked;

    fetch("getSessionID", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password,
        })
    }).then((response) => {
        if (!response.ok) {
            response.json().then((json) => {
                alert("Fejl: " + response.status + ", " + json["status"]);
            })
            return;
        }
            
        response.json().then((json) => {
            secureString = "";
            if (location.protocol === "https:" )
                secureString = " Secure;";

            if (rememberMe) {
                const date = new Date();
                date.setTime(date.getTime() + (json["expires"]));
                const expires = "expires=" + date.toUTCString();
                document.cookie = `SessionID=${json["session"]}; ${expires};${secureString} SameSite=Lax; path=/;`;
            } else {
                document.cookie = `SessionID=${json["session"]};${secureString} SameSite=Lax; path=/;`;
            }

            window.location.href = "shifts";
        });
    });
}
