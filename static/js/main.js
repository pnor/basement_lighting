const STATE_PERIOD = 1000;

// Periodically get state
get_state();
setInterval(get_state, STATE_PERIOD);

// Add event listeners
window.addEventListener("load", function() {
    var buttons = document.getElementsByClassName("button"); 
    for (i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener("click", start, false);
    }

    var btnStop = document.getElementsByClassName("stop")[0];
    btnStop.addEventListener("click", function(){ stop() });

    // Init color chooser with random color
    var colorInput = document.getElementById("colorInput");
    colorInput.value = random_hex_color();
});



function start(ev) {
    var xhr = new XMLHttpRequest();
    var path = ev.target.id;

    var colorInput = document.getElementById("colorInput");
    var color = colorInput.value;
    if (color == "" || color.toLowerCase() == "random") {
        color = random_hex_color();
    }

    var speedInput = document.getElementById("speedInput");
    var speed = speedInput.value;
    if (speed == "") {
        speed = 1;
    }

    var brightness = document.getElementById("brightnessInput").value;
    if (brightness == "") {
        brightness = 80;
    }
    if (brightness > 255) {
        brightness = 255;
    } else if (brightness < 0) {
        brightness = 0;
    }

    var post = { file: path, color: color, interval: speed, brightness: brightness };

    xhr.open("POST", `${URL}/control/start`, true);

    // Send start request
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send(JSON.stringify(post));
}

function stop() {
    var xhr = new XMLHttpRequest();

    xhr.open("POST", `${URL}/control/stop`, true);

    // Send stop request
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send( null );
}

function colorChange() {
    var xhr = new XMLHttpRequest();

    var colorInput = document.getElementById("colorInput");
    var color = colorInput.value;
    if (color == "" || color.toLowerCase() == "random") {
        color = random_hex_color();
    }

    var post = { color: color};

    xhr.open("POST", `${URL}/control/color`, true);

    // Send start request
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send(JSON.stringify(post));

}

function get_state() {
    fetch(`${URL}/state`)
        .then(res => res.json())
        .then(response => {
            var header = document.getElementsByTagName("header")[0]; 
            var title = document.getElementById("nowShowing"); 

            if (response.state == "RUNNING") {
                header.classList.add("header--active");
                header.classList.remove("header--ok");
                header.classList.remove("header--error");
                title.innerHTML = response.pattern;
            } else if (response.state == "GRACEFULLY_TERMINATED") {
                header.classList.remove("header--active");
                header.classList.add("header--ok");
                header.classList.remove("header--error");
                title.innerHTML = response.pattern;
            } else if (response.state == "CRASHED") {
                header.classList.remove("header--active");
                header.classList.remove("header--ok");
                header.classList.add("header--error");
                title.innerHTML = response.pattern;
            } else {
                header.classList.remove("header--active");
                header.classList.remove("header--ok");
                header.classList.remove("header--error");
                title.innerHTML = "N/A";
            }
        });
}

function random_hex_color() {
    return "#" + (Math.floor(Math.random() * 16777215).toString(16)).padStart(6, "0");
}
