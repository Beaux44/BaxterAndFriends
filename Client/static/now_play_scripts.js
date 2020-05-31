let current = ["", ""],
    next    = ["", ""],
    user_el = undefined,
    song_el = undefined,
    next_user = undefined,
    next_song = undefined,
    socket = undefined;

function updateDOM() {
    if(current[0] === "") {
        user_el.innerText = "No songs";
        song_el.innerText = "currently playing!";
    } else {
        user_el.innerText = current[0];
        song_el.innerText = current[1];
    }
    
    if(next[0] === "") {
        next_user.innerText = 'Use !sr';
        next_song.innerText = 'to request a song!';
    } else {
        next_user.innerText = next[0];
        next_song.innerText = next[1];
    }
}


document.addEventListener("DOMContentLoaded", function() {
    user_el = document.getElementById("user");
    song_el = document.getElementById("song");
    next_song = document.getElementById("nextUserSong");
    next_user = document.getElementById("nextUser");

    socket = new WebSocket("ws://localhost/now_playing");

    socket.onmessage = function(event) {
        let data = JSON.parse(event.data);
        if(data[0] === "") {
            current = next;
            next = data;
        } else {
            if(current[0] === "") {
                current = data;
            } else if(next[0] === "") {
                next = data;
            } else {
                current = next;
                next = data;
            }
        }
        updateDOM();
    };
});

