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
