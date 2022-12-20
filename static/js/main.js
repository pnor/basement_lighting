const URL = "http://127.0.0.1:5000"; 
const STATE_PERIOD = 1000;

// Periodically get state
get_state();
setInterval(get_state, STATE_PERIOD);

// Add click events to selectors
window.addEventListener("load", function() {
    var buttons = document.getElementsByClassName("button"); 

    for (i = 0; i < buttons.length; i++) {                                      
        buttons[i].addEventListener("click", start, false);
    }
});

// Add click events to selectors
window.addEventListener("load", function() {
    var btnStop = document.getElementsByClassName("stop")[0]; 

    btnStop.addEventListener("click", function(){ stop() });
});


function start(ev) {
    var xhr = new XMLHttpRequest();
    var path = ev.target.id;
    var post = { file: path, interval: 1 };

    xhr.open("POST", `${URL}/control/start`, true);

    // Send start request
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send(JSON.stringify(post));
}

function stop() {
    var xhr = new XMLHttpRequest();

    xhr.open("POST", `${URL}/control/stop`, true);

    // Send start request
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send( null );
}

function get_state() {
    fetch(`${URL}/state`)
        .then(res => res.json())
        .then(response => {
            var header = document.getElementsByTagName("header")[0]; 
            var title = document.getElementById("nowShowing"); 

            if (response.state == "RUNNING") {
                header.classList.add("header--active");
                header.classList.remove("header--error");
                title.innerHTML = response.pattern;
            } else if (response.state == "CRASHED") {
                header.classList.remove("header--active");
                header.classList.add("header--error");
                title.innerHTML = response.pattern;
            } else {
                header.classList.remove("header--active");
                header.classList.remove("header--error");
                title.innerHTML = "N/A";
            }
        });
}
