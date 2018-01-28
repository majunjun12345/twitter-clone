const log = function() {
    console.log.apply(console, arguments)
}

const _e = function(sel) {
    return document.querySelector(sel)
}

const ajax = {}

ajax.ajax = function(method, path, data, responseCallback) {
    let r = new XMLHttpRequest()
    r.open(method, path, true)
    r.setRequestHeader('Content-Type', 'application/json')
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            responseCallback(r.response)
        }
    }
    data = JSON.stringify(data)
    r.send(data)
}

ajax.get = function(path, data, responseCallback) {
    this.ajax('GET', path, data, responseCallback)
}

ajax.post = function(path, data, responseCallback) {
    this.ajax('POST', path, data, responseCallback)
}
