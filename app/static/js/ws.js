async function load_audio(container_id, audio_url, with_cropping_region = false, btns_container, make_visible, auto_play = true) {
    let container_div = $("#" + container_id);

    container_div.html("");

    let wavesurfer_options = {
        container: '#' + container_id,
        waveColor: 'white',
        progressColor: '#d64933',
        hideScrollbar: true
    };

    if (!!with_cropping_region)
        wavesurfer_options["plugins"] = [
            WaveSurfer.regions.create()
        ];

    let wavesurfer = WaveSurfer.create(wavesurfer_options);

    wavesurfer.load(audio_url);

    if (!!with_cropping_region) {
        // add region (for cropped audio) at center of recorded audio
        await new Promise(r => setTimeout(r, 100));
        let duration = wavesurfer.getDuration();
        wavesurfer.addRegion({
            start: duration * 2 / 5,
            end: duration * 3 / 5,
            color: 'hsla(100, 100%, 30%, 0.15)'
        });

        wavesurfer.on('region-click', function (region, e) {
            e.stopPropagation();
            region.play();
        });
    }

    if (!!auto_play)
        wavesurfer.play();

    let play_btn = btns_container.find(".play-btn");
    let pause_btn = btns_container.find(".pause-btn");

    play_btn.off();
    play_btn.on("click", function () {
        wavesurfer.play();
        toggle_play_btns(play_btn, pause_btn);
    });

    pause_btn.off();
    pause_btn.on("click", function () {
        wavesurfer.pause();
        toggle_play_btns(play_btn, pause_btn);
    });

    wavesurfer.on("finish", function () {
        play_btn.removeClass("btn-secondary").addClass("btn-success");
        pause_btn.removeClass("btn-success").addClass("btn-secondary");
    });

    setup_keybinds(btns_container);

    make_visible.forEach(function (element) {
        element.removeClass("invisible");
    });

    return wavesurfer;
}

function setup_keybinds(btns_container) {
    let body = $("body");

    body.off();
    body.keyup(function (e) {
        if (e.keyCode === 32 && e.target.tagName.toLowerCase() !== 'textarea') {
            btns_container.find(".play-btn").trigger("click");
            e.preventDefault();
        }
    });

    $(document).off();
    $(document).keydown(function (e) {
        if (e.which === 32 && e.target.tagName.toLowerCase() !== 'textarea') {
            return false;
        }
    });
}

function toggle_play_btns(play_btn, pause_btn) {
    if (play_btn.hasClass("btn-success")) {
        play_btn.removeClass("btn-success").addClass("btn-secondary");
        pause_btn.removeClass("btn-secondary").addClass("btn-success");
    } else {
        play_btn.removeClass("btn-secondary").addClass("btn-success");
        pause_btn.removeClass("btn-success").addClass("btn-secondary");
    }
}