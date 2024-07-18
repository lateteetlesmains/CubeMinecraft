function sendColor() {
    var colorPicker = document.getElementById("colorPicker");
    var brightnessInput = document.getElementById("brightness");

    if (colorPicker && brightnessInput) {
        var color = colorPicker.value;
        var brightness = brightnessInput.value;
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/set_color?color=" + color.substring(1) + "&brightness=" + brightness, true);
        xhr.send();
    } else {
        console.error("Color picker or brightness input not found.");
    }
}

function adjustBrightness() {
    var colorPicker = document.getElementById("colorPicker");
    var brightnessInput = document.getElementById("brightness");

    if (colorPicker && brightnessInput) {
        var color = colorPicker.value;
        var brightness = brightnessInput.value;
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/set_brightness?color=" + color.substring(1) + "&brightness=" + brightness, true);
        xhr.send();
    } else {
        console.error("Color picker or brightness input not found.");
    }
}

