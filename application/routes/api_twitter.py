from application.routes import current_user, json_response

from application.models.twitter import Twitter

from utils import log


def all(request):
    twitters = Twitter.all_json()
    return json_response(twitters)


def add(request):
    form = request.json()
    user_id = current_user(request).id
    w = Twitter.new(form, user_id)
    return json_response(w.json())


def delete(request):
    twitter_id = int(request.query.get('id'))
    t = Twitter.delete(twitter_id)
    return json_response(t.json())


def update(request):
    form = request.json()
    twitter_id = int(form.get('id'))
    t = Twitter.update(twitter_id, form)
    return json_response(t.json())
