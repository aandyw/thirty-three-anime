const SELECT_ENDPOINT = 'http://127.0.0.1:8000/select';
const MATRIX_VIEW = document.querySelector(".matrix");

let select_anime = (title, image_url) => {

    var request = new XMLHttpRequest();
    let url = new URL(SELECT_ENDPOINT);
    url.searchParams.set('title', title);
    url.searchParams.set('image_url', image_url);

    request.open('GET', url, true);

    request.onload = function () {
        if (this.status >= 200 && this.status < 400) {
            // Success!
            var data = JSON.parse(this.response);
            console.log(data);
            MATRIX_VIEW.innerHTML = data['html_view'];

        } else {
            // We reached our target server, but it returned an error
            console.log(this.status);
        }
    };

    request.onerror = function () {
        // There was a connection error of some sort
    };

    console.log("SENDING SELECTION REQUEST");
    request.send();
};
