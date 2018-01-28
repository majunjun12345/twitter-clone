from application.models.comment import Comment

from application.routes import current_user, json_response

from utils import log


def all(request):
    twitter_id = int(request.query.get('twitter_id'))
    cs = Comment.find_all(twitter_id=twitter_id)
    cs_json = [c.json() for c in cs]
    return json_response(cs_json)


def add(request):
    u = current_user(request)
    form = request.json()
    c = Comment.new(form, u.id)
    return json_response(c.json())


def delete(request):
    comment_id = int(request.query.get('id'))
    c = Comment.delete(comment_id)
    return json_response(c.json())


def update(request):
    form = request.json()
    id = int(form.get('id'))
    t = Comment.update(id, form)
    return json_response(t.json())
