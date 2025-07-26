updateShifts();

function updateShifts() {
    const shiftList = document.getElementById("shifts");

    fetch("/shifts").then((response) => {
        response.json().then((data) => {
            console.log(data);
        })
    })
}

function addShift() {

}