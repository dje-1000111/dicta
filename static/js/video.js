var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
var player;

function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        height: '95%',
        width: '95%',
        videoId: vid,
        host: 'https://www.youtube-nocookie.com',
        playerVars: {
            controls: 0,
            cc_load_policy: 0,
            showinfo: 1,
            autoplay: 0,
            autohide: 1,
            playsinline: 1,
            start: ts[lineNb],
            fs: 0,
        },
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}

function onPlayerReady(event) {
    event.target.pauseVideo();
}

var paused = true
var done = false;

function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING) {
        iplaystop.classList.replace('fa-play', 'fa-stop')
        const checkTime = setInterval(() => {
            if (player.getCurrentTime() >= ts[lineNb + 1]) {
                player.pauseVideo();
                clearInterval(checkTime);
            }

        }, 100);
    }
    if (event.data == YT.PlayerState.PAUSED && !done) {
        iplaystop.classList.replace('fa-stop', 'fa-play')
        done = false;
        paused = true
    }
}

function playSegment() {
    if (lineNb < ts.length - 1) {
        player.seekTo(ts[lineNb]);
        setTimeout(() => {
            player.playVideo();
        }, 200);
        paused = false
        done = true
    }
}

function pauseSegment() {
    player.pauseVideo();
}

function playCurrent() {
    playSegment();
}

function playPrevious() {
    if (lineNb > 0) {
        lineNb--;
        player.seekTo(ts[lineNb]);
        setTimeout(() => {
            player.playVideo();
        }, 200);
        paused = false
        done = false
    }
}

function playNext() {
    if (lineNb < ts.length - 2) {
        lineNb++;
        player.seekTo(ts[lineNb]);
        setTimeout(() => {
            player.playVideo();
        }, 200);
        paused = false
        done = false
    }
}
