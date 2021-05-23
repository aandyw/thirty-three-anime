const SELECT_ENDPOINT = 'http://127.0.0.1:8000/select';
const RECOMMEND_ENDPOINT = 'http://127.0.0.1:8000/recommend';
const MATRIX_VIEW = document.querySelector(".matrix");

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

let recommend = () =>{
    var request = new XMLHttpRequest();
    let url = new URL(RECOMMEND_ENDPOINT);
    request.open('GET', url, true);

    request.onload = function () {
        if (this.status >= 200 && this.status < 400) {
            // Success!
            console.log("success");

        } else {
            // We reached our target server, but it returned an error
            console.log(this.status);
        }
    };

    request.onerror = function () {
        // There was a connection error of some sort
    };

    request.send();
}
