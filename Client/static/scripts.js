var socket = new WebSocket("ws://localhost/client");
let queue = [];

socket.onopen = function(event) {
    socket.send(JSON.stringify({event: "CONNECT"}));
    nextSong();
};

function requestData(data) {
    return data || ["", ""];
}

function nextSong() {
    queue.shift();
    socket.send(JSON.stringify({
        event: "SONG",
        song: requestData(queue[1]),
    }));
    setTimeout(nextSong, 15000);
}

socket.onmessage = function(event) {
    let data = JSON.parse(event.data);
    switch(data.event) {
        case "REQUEST":
            console.log("GOT REQUEST NOODLY DOO");
            queue.push([data.req.user, data.req.req]);
            if(queue.length <= 2)
                socket.send(JSON.stringify({
                    event: "SONG",
                    song: requestData(queue[queue.length-1]),
                }));
            break;
        case "JOIN":
            socket.send(JSON.stringify([requestData(queue[0]), requestData(queue[1])]));
            break;
    }
};


function updateSlider(val) {
    let span = val.childNodes[2];
    let input = val.childNodes[1];

    input.oninput = function() {
        span.innerText=input.value;
    };
    input.oninput();

    input.onmouseup = function() {
        let {id, value} = input;
        console.log(id);
        socket.send(JSON.stringify({event: "UPD_SLIDER", name: id, value: parseInt(value)}));
    };
}


// Update the current slider value (each time you drag the slider handle)
document.addEventListener("DOMContentLoaded", function() {
    let sounds_slider = document.getElementById("sounds-cooldown");
    let tts_slider = document.getElementById("tts-max-chars");
    console.log(sounds_slider, tts_slider);
    updateSlider(sounds_slider);
    updateSlider(tts_slider);
});

