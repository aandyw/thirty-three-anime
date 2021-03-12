const USER_INPUT = $("#user-input");
const SEARCH_ICON = $('#search-icon');
const ANIME_DIV = $('#replaceable-content');
const ENDPOINT = '';
const DELAY_MS = 500;
let scheduled_function = false;

let ajax_call = (endpoint, request_parameters) => {
    $.getJSON(endpoint, request_parameters)
        .done(response => {
            // fade out the artists_div, then:
            ANIME_DIV.fadeTo('slow', 0).promise().then(() => {
                // replace the HTML contents
                ANIME_DIV.html(response['html_view']);
                // fade-in the div with new contents
                ANIME_DIV.fadeTo('slow', 1);
                // stop animating search icon
                SEARCH_ICON.removeClass('blink');
            });
        });
};

USER_INPUT.on('keyup', () => {

    const request_parameters = {
        q: USER_INPUT.val() // get input from search
    };
    // start animating the search icon with the CSS class
    SEARCH_ICON.addClass('blink');

    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function);
    }

    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(ajax_call, DELAY_MS, ENDPOINT, request_parameters);
});