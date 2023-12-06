let currentButton = null;

function changeColor(button) {
    if (currentButton !== null) {
        currentButton.classList.remove("pressed");
    }

    currentButton = button;

    currentButton.classList.add("pressed");
}