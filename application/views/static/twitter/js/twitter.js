'use strict'

let twitterTemplate = function(twitter) {
    let t = `
        <li class="twitter-cell js-stream-item stream-item stream-item">
            <div class="tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content
original-tweet js-original-tweet has-cards dismissible-content has-content">
                <div class="context"></div>

                <div class="content">
                    <div class="stream-item-header">
                        <a class="account-group js-account-group js-action-profile js-user-profile-link js-nav"
                           href="#">
                            <img class="avatar js-action-profile-avatar"
                                 src="/twitter/static/twitter/img/avatar.png">
                            <span class="username u-dir u-textTruncate"
                                  dir="ltr">@<b>${_username()}</b></span>
                        </a>
                    </div>

                    <div class="js-tweet-text-container">
                        <p class="twitter-content TweetTextSize js-tweet-text tweet-text" lang="zh">${twitter.content}</p>
                    </div>
                </div>
                <div class="twitter-button">
                    <button type="button" data-twitter-id=${twitter.id} class="twitter-delete btn btn-primary btn-sm float-right">删除</button>
                    <button type="button" data-twitter-id=${twitter.id} class="twitter-edit btn btn-primary btn-sm float-right">编辑</button>
                </div>
                <hr />
                <div class="comment">
                    <div data-twitter-id=${twitter.id} class="comment-list-${twitter.id}"></div>
                    <input data-twitter-id=${twitter.id} class="comment-input RichEditor" name="content">
                    <button type="button" data-twitter-id=${twitter.id} class="comment-add btn btn-primary btn-sm" type="submit">添加评论</button>
                </div>
            </div>
        </li>
    `
    return t
}

let twitterEditForm = function(twitterId) {
    let t = `
        <div class="twitter-update-form">
            <input class="twitter-update-input RichEditor">
            <button type="button" data-twitter-id=${twitterId} class="twitter-update btn btn-outline-primary btn-sm">更新</button>
        </div>
    `
    return t
}

let insertTwitter = function(twitter) {
    let twitterCell = twitterTemplate(twitter)
    let twitterList = _e('.twitter-list')
    twitterList.insertAdjacentHTML('beforeend', twitterCell)
}

let insertTwitterUpdate = function(edit_button) {
    let twitterId = edit_button.dataset.twitterId
    let editCell = twitterEditForm(twitterId)
    edit_button.parentElement.insertAdjacentHTML('beforeend', editCell)
}

let bindEventTwitterAdd = function() {
    let b = _e('#id-button-add')
    b.addEventListener('click', function() {
        let div = _e('#id-div-twitter')
        let content = div.textContent
        let form = {
            content: content,
        }
        apiTwitterAdd(form, function(r) {
            let twitter = JSON.parse(r)
            insertTwitter(twitter)
        })
    })
}

let bindEventTwitterDelete = function() {
    let twitterList = _e('.twitter-list')
    twitterList.addEventListener('click', function(event) {
        let self = event.target
        if(self.classList.contains('twitter-delete')) {
            log('点到了 删除按钮，id 是', self.dataset.twitterId)
            let twitterId = self.dataset.twitterId
            apiTwitterDelete(twitterId, function() {
                self.parentElement.parentElement.remove()
            })
        } else {
            log('点击的不是删除按钮******')
        }
    })
}

let bindEventTwitterEdit = function() {
    let twitterList = _e('.twitter-list')
    twitterList.addEventListener('click', function(event) {
        let self = event.target
        if(self.classList.contains('twitter-edit')) {
            log('点到了 编辑按钮，id 是', self.dataset.twitterId)
            insertTwitterUpdate(self)
        } else {
            log('点击的不是编辑按钮******')
        }
    })
}

let bindEventTwitterUpdate = function() {
    let twitterList = _e('.twitter-list')
    twitterList.addEventListener('click', function(event) {
        let self = event.target
        if(self.classList.contains('twitter-update')) {
            log('点到了 更新按钮，id 是', self.dataset.twitterId)
            
            let twitterCell = self.closest('.twitter-cell')
            let input = twitterCell.querySelector('.twitter-update-input')
            let twitterId = self.dataset.twitterId
            let form = {
                id: twitterId,
                content: input.value,
            }
            
            apiTwitterUpdate(form, function(r) {
                log('收到更新数据', r)
                
                let updateForm = twitterCell.querySelector('.twitter-update-form')
                updateForm.remove()
                
                let twitter = JSON.parse(r)
                let twitterContent = twitterCell.querySelector('.twitter-content')
                twitterContent.innerText = twitter.content
            })
        } else {
            log('点击的不是更新按钮******')
        }
    })
}

let loadTwitters = function(r) {
    let twitters = JSON.parse(r)
    for(let i = 0; i < twitters.length; i++) {
        let twitter = twitters[i]
        insertTwitter(twitter)
    }
}

var loadContent = function() {
    apiTwitterAll(function(r) {
        loadTwitters(r)
        loadComments()
    })
}

let bindTwitterEvents = function() {
    bindEventTwitterAdd()
    bindEventTwitterDelete()
    bindEventTwitterEdit()
    bindEventTwitterUpdate()
}

let bindEvents = function() {
    bindTwitterEvents()
    bindCommentEvents()
}

let __main = function() {
    bindEvents()
    loadContent()
}

__main()

