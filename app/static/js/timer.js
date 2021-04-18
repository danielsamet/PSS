// Adapted from code by Macek, https://stackoverflow.com/questions/20318822/how-to-create-a-stopwatch-using-javascript
let Stopwatch = function (elem, options) {

    let timer = createTimer(),
        offset,
        clock,
        interval;

    // default options
    options = options || {};
    options.delay = options.delay || 1;

    // append elements
    elem.appendChild(timer);

    // initialize
    reset();

    // private functions
    function createTimer() {
        return document.createElement("span");
    }

    function start() {
        if (!interval) {
            offset = Date.now();
            interval = setInterval(update, options.delay);
        }
    }

    function stop() {
        if (interval) {
            clearInterval(interval);
            interval = null;
        }
    }

    function reset() {
        clock = 0;
        render(0);
    }

    function update() {
        clock += delta();
        render();
    }

    function render() {
        timer.innerHTML = (Math.round(clock / 1000 * 100) / 100).toFixed(2);
    }

    function delta() {
        let now = Date.now(),
            d = now - offset;

        offset = now;
        return d;
    }

    // public API
    this.start = start;
    this.stop = stop;
    this.reset = reset;
};