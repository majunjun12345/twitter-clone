from application.models.comment import Comment
from application.models.user import User
from application.models.twitter import Twitter

from application.routes import current_user, redirect, http_response

from utils import template, log


def index(request):
    u = current_user(request)
    if u is None:
        u = {
            'username': 'guest'
        }
    
    body = template('twitter/index.html', user=u)
    return http_response(body)
