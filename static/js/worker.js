self.onmessage = function (e) {
    const intervals = e.data; // Array of intervals in milliseconds
    intervals.forEach((interval, index) => {
        setTimeout(() => {
            self.postMessage('stop');
        }, interval);
    });
};