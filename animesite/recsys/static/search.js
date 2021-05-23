const USER_INPUT = document.querySelector("#user-input");
const SEARCH_ICON = document.querySelector("#search-icon");
const ANIME_DIV = document.querySelector("#cards");
const SEARCH_ENDPOINT = 'http://127.0.0.1:8000/animes';
const DELAY_MS = 500;
let scheduled_function = false;

// FADE OUT
function fadeOut(el) {
    return new Promise(function (resolve, reject) {
        var fadeEffect = setInterval(function () {
            if (!el.style.opacity) {
                el.style.opacity = 1;
            }
            if (el.style.opacity > 0) {
                el.style.opacity -= 0.1;
            } else {
                clearInterval(fadeEffect);
                resolve();
            }
        }, 10);
    });

}

// FADE IN
function fadeIn(el, duration = 250) {
    el.style.display = '';
    el.style.opacity = 0;
    var last = +new Date();
    var tick = function () {
        el.style.opacity = +el.style.opacity + (new Date() - last) / duration;
        last = +new Date();
        if (+el.style.opacity < 1) {
            (window.requestAnimationFrame && requestAnimationFrame(tick)) || setTimeout(tick, 16);
        }
    };
    tick();
}


let ajax_call = (endpoint, req_params) => {

    var request = new XMLHttpRequest();
    let url = new URL(endpoint);
    url.searchParams.set('q', req_params);

    request.open('GET', url, true);

    request.onload = function () {
        if (this.status >= 200 && this.status < 400) {
            // Success!
            var data = JSON.parse(this.response);
            fadeOut(ANIME_DIV).then(() => {
                ANIME_DIV.innerHTML = data['html_view'];
                fadeIn(ANIME_DIV);
            });

        } else {
            // We reached our target server, but it returned an error
            console.log(this.status);
        }
    };

    request.onerror = function () {
        // There was a connection error of some sort
    };

    request.send();
};

USER_INPUT.addEventListener('keyup', (event) => {
    const req_params = USER_INPUT.value;
    // start animating the search icon with the CSS class
    // SEARCH_ICON.addClass('blink');

    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function);
    }

    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(ajax_call, DELAY_MS, SEARCH_ENDPOINT, req_params);
});