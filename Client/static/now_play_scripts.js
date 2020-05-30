let current = ["", ""],
    next    = ["", ""],
    user_el = undefined,
    song_el = undefined,
    next_user = undefined,
    next_song = undefined,
    socket = undefined;

function updateDOM() {
    user_el.innerText = current[0];
    song_el.innerText = current[1];
    next_user.innerText = next[0];
    next_song.innerText = next[1];
}


document.addEventListener("DOMContentLoaded", function() {
    user_el = document.getElementById("user");
    song_el = document.getElementById("song");
    next_song = document.getElementById("nextUserSong");
    next_user = document.getElementById("nextUser");

    socket = new WebSocket("ws://localhost/now_playing");

    socket.onmessage = function(event) {
        current = next;
        next = JSON.parse(event.data);
        updateDOM();
    };
});

