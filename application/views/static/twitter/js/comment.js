'use strict'

let commentTemplate = function(comment) {
    let t = `
        <div class="comment-cell-${comment.id}">
            <span class="comment-content-${comment.id}">${comment.content}</span>
            <div class="comment-button">
                <button data-twitter-id=${comment.twitter_id} data-comment-id=${comment.id} class="comment-delete btn btn-primary btn-sm">删除</button>
                <button data-twitter-id=${comment.twitter_id} data-comment-id=${comment.id} class="comment-edit btn btn-primary btn-sm">编辑</button>
            </div>
        </div>
    `
    return t
}

let commentEditForm = function(commentId) {
    let t = `
        <div class="comment-update-form">
            <input class="comment-update-input RichEditor">
            <button data-comment-id=${commentId} class="comment-update btn btn-primary btn-sm">更新</button>
        </div>
    `
    return t
}

let insertComment = function(comment) {
    let commentCell = commentTemplate(comment)
    let commentList = _e(`.comment-list-${comment.twitter_id}`)
    commentList.insertAdjacentHTML('beforeend', commentCell)
}

let insertCommentUpdate = function(edit_button) {
    let commentId = edit_button.dataset.commentId
    let editCell = commentEditForm(commentId)
    edit_button.parentElement.insertAdjacentHTML('afterend', editCell)
}

let bindEventcommentAdd = function() {
    let twitterList = _e('.twitter-list')
    twitterList.addEventListener('click', function(event) {
        let self = event.target
        if(self.classList.contains('comment-add')) {
            log('点到了 comment 的添加按钮，对应的 twitter_id 是', self.dataset.twitterId)
            
            let twitterId = self.dataset.twitterId
            let input = event.target.parentElement.querySelector('.comment-input')
            let content = input.value
            
            let form = {
                twitter_id: twitterId,
                content: content,
            }
            
            apiCommentAdd(form, function(r) {
                log("apiCommentAdd", r)
                let comment = JSON.parse(r)
                insertComment(comment)
                input.value = ''
            })
        } else {
            log('点击的不是 comment 的添加按钮')
        }
    })
}

let bindEventCommentDelete = function() {
    let twitterList = _e('.twitter-list')
    twitterList.addEventListener('click', function(event) {
        let self = event.target
        if(self.classList.contains('comment-delete')) {
            log('点击了 comment delete, id:', self.dataset.commentId)
            
            let commentId = self.dataset.commentId
            apiCommentDelete(commentId, function(r) {
                let comments = JSON.parse(r)
                
                if(comments.id = commentId) {
                    self.parentElement.parentElement.remove()
                }
            })
        } else {
            log('点击的不是 comment 的删除按钮')
        }
    })
}

let bindEventCommentEdit = function() {
    let twitterList = _e('.twitter-list')
    twitterList.addEventListener('click', function(event) {
        let self = event.target
        if(self.classList.contains('comment-edit')) {
            log('点到了 编辑按钮，id 是', self.dataset.commentId)
            insertCommentUpdate(self)
        } else {
            log('点击的不是 comment 的编辑按钮')
        }
    })
}

let bindEventCommentUpdate = function() {
    let twitterList = _e('.twitter-list')
    twitterList.addEventListener('click', function(event) {
        let self = event.target
        if(self.classList.contains('comment-update')) {
            log('点到了 comment 的更新按钮，comment id 是', self.dataset.commentId)
            let commentId = self.dataset.commentId
            let commentCell = self.closest(`.comment-cell-${commentId}`)
            let input = commentCell.querySelector('.comment-update-input')
            let content = input.value
            
            let form = {
                id: commentId,
                content: content,
            }
            
            log('form', form)
            
            apiCommentUpdate(form, function(r) {
                log('收到更新数据', r)
                
                let updateForm = commentCell.querySelector('.comment-update-form')
                updateForm.remove()
                
                let comment = JSON.parse(r)
                let commentContent = commentCell.querySelector(`.comment-content-${commentId}`)
                log('commentContent', commentContent)
                commentContent.innerText = comment.content
            })
        } else {
            log('点击的不是更新按钮******')
        }
    })
}

let loadComments = function() {
    let commentLists = document.querySelectorAll('[class^="comment-list"]')
    commentLists = Array.from(commentLists)
    
    for(let i in commentLists) {
        let id = commentLists[i].dataset.twitterId
        apiCommentAll(id, function(r) {
            let comments = JSON.parse(r)
            
            for(let j in comments) {
                let c = comments[j]
                insertComment(c)
            }
        })
    }
}

let bindCommentEvents = function() {
    bindEventcommentAdd()
    bindEventCommentDelete()
    bindEventCommentEdit()
    bindEventCommentUpdate()
}
