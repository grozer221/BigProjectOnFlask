let song = new Audio();
window.onload = function () {
    let listSongs = document.querySelectorAll('.song');
    let songsHtml = document.querySelectorAll('.nameSongSn');
    let controls = document.querySelector('.player')
    let audios = document.querySelectorAll('audio');
    let id_song; //вибрана пісня по ід
    let song; //пісня, яка містить в собі обєкт аудіо
    let mute = false; //звук вкл або викл
    let volume = 0.2; //керування звуком
    let songs = {};//обєкт пісень
    for (let i = 0; i < songsHtml.length; i++) {
        songs[i.toString()] = {
            id: i,
            name: songsHtml[i].innerText,
            src: audios[i].children[0].src,
            totalPlay: ''
        }
    }
    for (let i = 0; i < listSongs.length; i++) {
        listSongs[i].id = i.toString();
        let song = new Audio(songs[i].src)
        song.addEventListener('loadedmetadata', function () {
            let seconds = this.duration
            let time = parseInt(seconds / 60) + ':';
            if (parseInt(seconds % 60) === 0) {
                time += parseInt(seconds % 60) + '0';
            } else {
                time += parseInt(seconds % 60);
            }
            listSongs[i].children[3].innerText = time;
        });
    }

    function playNewSong(id) {
        let currTime;//час, який іде в секундах
        let current = -100;//для подвигання прогрес бара
        controls.children[1].innerText = songs[id].name;
        controls.children[0].id = id;
        id_song = id;
        song = new Audio(songs[id].src);
        controls.children[0].innerText = '⏸';
        listSongs[id].children[0].innerText = '⏸';
        song.play();
        song.volume = volume;
        song.addEventListener('timeupdate', function () {
            currTime = song.currentTime;
            current = -((this.duration - currTime) * 100) / this.duration;
            if (parseInt(currTime % 60) < 10) {
                controls.children[4].innerText = parseInt(currTime / 60) + ':0' + parseInt(currTime % 60);

            } else {
                controls.children[4].innerText = parseInt(currTime / 60) + ':' + parseInt(currTime % 60);
            }
            controls.children[3].children[1].children[0].style.left = current + '%';
        });
    }

    function allPause() {
        for (let i = 0; i < listSongs.length; i++) {
            listSongs[i].children[0].innerText = '▶'
        }
    }

    for (let i = 0; i < listSongs.length; i++) {
        listSongs[i].addEventListener('click', function () {
            let id = this.id;
            listSongs[id].children[0].innerText = '▶'
            allPause();
            playPauseSong(id);
            id++;
            controls.children[2].children[1].dataset.id = id;
            id--;
            id--;
            controls.children[2].children[0].dataset.id = id;
        });
    }
    controls.children[0].addEventListener('click', function () {
        let id = this.id;
        listSongs[id].children[0].innerText = '▶'
        allPause();
        playPauseSong(id);
    });
    controls.children[2].children[0].addEventListener('click', function () {
        let id = this.dataset.id;
        if (id != -1) {
            allPause();
            playPauseSong(id);
            id++;
            controls.children[2].children[1].dataset.id = id;
            id--;
            id--;
            controls.children[2].children[0].dataset.id = id;
        }
    });

    controls.children[2].children[1].addEventListener('click', function () {
        let id = this.dataset.id;
        if (id != -1 || id != (listSongs.length)) {
            allPause();
            playPauseSong(id);
            id++;
            controls.children[2].children[1].dataset.id = id;
            id--;
            id--;
            controls.children[2].children[0].dataset.id = id;
        }
    });

    function playPauseSong(id) {
        if (song) {
            if (id == id_song) {
                if (song.paused) {
                    song.play();
                    song.volume = volume;
                    controls.children[0].innerText = '⏸'
                    listSongs[id].children[0].innerText = '⏸'
                } else {
                    song.pause();
                    controls.children[0].innerText = '▶'
                    listSongs[id].children[0].innerText = '▶'
                }
            } else {
                song.pause()
                controls.children[0].innerText = '▶'
                listSongs[id].children[0].innerText = '▶'
                playNewSong(id);
            }
        } else {
            controls.children[0].innerText = '⏸'
            listSongs[id].children[0].innerText = '▶'
            playNewSong(id);
        }
    }

    controls.children[2].children[2].addEventListener('click', function () {
        if (song) {
            if (mute == false) {
                mute = true;
                controls.children[2].children[2].innerText = '🔇';
                controls.children[2].children[3].value = 0;
                volume = 0;
            } else {
                mute = false;
                controls.children[2].children[2].innerText = '🔈';
                controls.children[2].children[3].value = 100;
            }
            song.muted = mute;
        }
    });

    controls.children[2].children[3].addEventListener('change', function () {
        let value = this.value;
        if (song) {
            volume = value / 100;
            song.volume = volume;
            if (value == 0) {
                mute = true;
                controls.children[2].children[2].innerText = '🔇';
            } else if (value > 0) {
                mute = false;
                controls.children[2].children[2].innerText = '🔈';
            }
        }
    });
    controls.children[3].children[1].addEventListener('mouseenter', function () {
        if (song) {
            let id = controls.children[0].id;


        }
    });
    controls.children[3].children[1].addEventListener('click', function (e) {
        let offset = this.offsetTop;
        let duration = song.duration;
        let width = screen.width;
        let x = e.pageX - offset;
        console.log(x);
        let xproc = (x * 100) / width;
        let sec = (xproc * duration);
        sec = sec / 100;
        xproc = xproc - 100;
        controls.children[3].children[1].children[0].style.left = xproc + '%';
        song.currentTime = sec;
    });
}
