let apiTwitterAll = function(callback) {
    let path = '/twitter/twitter/all'
    ajax.get(path, '', callback)
}

let apiTwitterAdd = function(form, callback) {
    let path = '/twitter/twitter/add'
    ajax.post(path, form, callback)
}

let apiTwitterDelete = function(id, callback) {
    let path = `/twitter/twitter/delete?id=${id}`
    ajax.get(path, '', callback)
}

let apiTwitterUpdate = function(form, callback) {
    let path = '/twitter/twitter/update'
    ajax.post(path, form, callback)
}

let apiCommentAll = function(TwitterId, callback) {
    let path = `/twitter/comment/all?twitter_id=${TwitterId}`
    ajax.get(path, '', callback)
}

let apiCommentAdd = function(form, callback) {
    let path = '/twitter/comment/add'
    ajax.post(path, form, callback)
}

let apiCommentDelete = function(CommentId, callback) {
    let path = `/twitter/comment/delete?id=${CommentId}`
    ajax.get(path, '', callback)
}

let apiCommentUpdate = function(form, callback) {
    let path = '/twitter/comment/update'
    ajax.post(path, form, callback)
}
