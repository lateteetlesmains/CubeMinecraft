function sendColor() {
    var color = document.getElementById("colorPicker").value;
            var brightness = document.getElementById("brightness").value;
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/set_color?color=" + color.substring(1) + "&brightness=" + brightness, true);
            xhr.send();
   
}

function adjustBrightness() {
     var color = document.getElementById("colorPicker").value;
            var brightness = document.getElementById("brightness").value;
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/set_brightness?color=" + color.substring(1) + "&brightness=" + brightness, true);
            xhr.send();
}
