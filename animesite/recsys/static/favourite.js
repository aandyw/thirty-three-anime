const ENDPOINT = 'http://127.0.0.1:8000/fav';

let fav_select = (endpoint, req_params) => {

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
