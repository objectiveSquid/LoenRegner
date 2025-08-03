function logout() {
    fetch("logout", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    }).then((response) => {
        if (!response.ok) {
            response.json().then((json) => {
                alert("Error: " + response.status + ", " + json["status"]);
            })
            return;
        }
    })

    document.cookie = "SessionID=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    window.location.href = "login";
}

function deleteAccount() {
    if (prompt('Er du sikker på at du vil slette din konto?  Skriv "Jeg vil gerne slette min konto." for at bekræfte.', "") !== "Jeg vil gerne slette min konto.") {
        alert("Kontoen blev ikke slettet.");
        return;
    }

    fetch("deleteAccount", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    }).then((response) => {
        if (!response.ok) {
            response.json().then((json) => {
                alert("Error: " + response.status + ", " + json["status"]);
                window.location.href = "login"; // If the account failed to delete: the login will redirect back to the shifts page. But if it succeeded: it will stay at the login page.
                return;
            })

        }
        // successfully deleted account
        document.cookie = "SessionID=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        window.location.href = "login";
        return;
    })
    
}

function changePassword() {
    const oldPassword = document.getElementById("oldPassword").value;
    const newPassword = document.getElementById("newPassword").value;

    fetch("changePassword", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            oldPassword: oldPassword,
            newPassword: newPassword,
        })
    }).then((response) => {
        if (!response.ok) {
            response.json().then((json) => {
                alert("Error: " + response.status + ", " + json["status"]);
            })
            return;
        }
    })
}