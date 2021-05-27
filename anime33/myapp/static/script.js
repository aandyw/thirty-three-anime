const USER_INPUT = document.querySelector("#user-input");
const SEARCH_ICON = document.querySelector("#search-icon");
const ANIME_DIV = document.querySelector("#cards");
const SUBMIT_BUTTON = document.querySelector("#submit");
const CLEAR_BUTTON = document.querySelector("#clear");
const MATRIX_VIEW = document.querySelector(".matrix");

// endpoints
const SEARCH_ENDPOINT = 'http://127.0.0.1:8000/animes';
const SELECT_ENDPOINT = 'http://127.0.0.1:8000/select';
const RECOMMEND_ENDPOINT = 'http://127.0.0.1:8000/predictor/recommend';
const CLEAR_ENDPOINT = 'http://127.0.0.1:8000/clear';

const DELAY_MS = 500;
let scheduled_function = false;

const LOADER_HTML = '<div class="lds-grid"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>';

/* EFFECTS */

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

/* calls */

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

let select_anime = (id, title, image_url) => {

    var request = new XMLHttpRequest();
    let url = new URL(SELECT_ENDPOINT);

    url.searchParams.set('id', id);
    url.searchParams.set('title', title);
    url.searchParams.set('image_url', image_url);

    request.open('GET', url, true);

    request.onload = function () {
        if (this.status >= 200 && this.status < 400) {
            // Success!
            var data = JSON.parse(this.response);
            MATRIX_VIEW.innerHTML = data['html_view'];
            console.log("Selected anime data: " + data);
        } else {
            // We reached our target server, but it returned an error
            console.log("select error: " + this.status);
        }
    };

    request.onerror = function () {
        // There was a connection error of some sort
    };

    console.log("SENDING SELECTION REQUEST");
    request.send();
};

SUBMIT_BUTTON.addEventListener('click', (event) => {
    document.body.innerHTML = LOADER_HTML;

    var request = new XMLHttpRequest();
    let url = new URL(RECOMMEND_ENDPOINT);
    request.open('GET', url, true);

    request.onload = function () {
        if (this.status >= 200 && this.status < 400) {
            // Success!
            var data = JSON.parse(this.response);
            document.body.innerHTML = data['html_view'];
            fadeIn(document.body);
            console.log("recommendation success");
        } else {
            // We reached our target server, but it returned an error
            console.log("recommendation error: " + this.status);
        }
    };

    request.onerror = function () {
        // There was a connection error of some sort
    };

    request.send();
});

CLEAR_BUTTON.addEventListener('click', (event) => {
    var request = new XMLHttpRequest();
    let url = new URL(CLEAR_ENDPOINT);
    request.open('GET', url, true);

    request.onload = function () {
        if (this.status >= 200 && this.status < 400) {
            // Success!
            var data = JSON.parse(this.response);
            MATRIX_VIEW.innerHTML = data['html_view'];
            console.log("matrix clear success");
        } else {
            // We reached our target server, but it returned an error
            console.log("matrix clear error: " + this.status);
        }
    };

    request.onerror = function () {
        // There was a connection error of some sort
    };

    request.send();
});