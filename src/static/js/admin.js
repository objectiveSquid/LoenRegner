function logoutAdmin() {
    document.cookie = "SessionID=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    window.location.href = "login";
}

function deleteAccountAdmin(uuid) {
    if (prompt('Er du sikker på at du vil slette denne konto?  Skriv "Jeg vil gerne slette denne konto." for at bekræfte.', "") !== "Jeg vil gerne slette denne konto.") {
        alert("Kontoen blev ikke slettet.");
        return;
    }

    fetch("deleteAccountAdmin", {
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
                return;
            })
        }

        window.location.reload();
        return;
    })
}

function loginAsUserAdmin(uuid) {
    fetch("getSessionIDAdmin", {
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
                return;
            })
        }

        response.json().then((json) => {
            secureString = "";
            if (location.protocol === "https:" )
                secureString = " Secure;";

            document.cookie = `SessionID=${json["session"]};${secureString} SameSite=Lax; path=/;`;

            window.location.href = "shifts";
        });
    })
}

function changeUserPasswordAdmin(uuid) {
    // lazy element naming, i know
    const newPassword = document.getElementById(uuid).value;

    if (prompt('Er du sikker på at du vil ændre denne kontos adgangskode?  Skriv "Jeg vil gerne ændre denne adgangskode." for at bekræfte.', "") !== "Jeg vil gerne ændre denne adgangskode.") {
        alert("Adgangskoden blev ikke ændret.");
        return;
    }

    fetch("changePasswordAdmin", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            uuid: uuid,
            newPassword: newPassword,
        })
    }).then((response) => {
        if (!response.ok) {
            response.json().then((json) => {
                alert("Fejl: " + response.status + ", " + json["status"]);
                return;
            })
        }

        window.location.reload();
        return;
    })
}