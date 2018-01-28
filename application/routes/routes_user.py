import uuid

from application.models.session import Session
from application.models.user import User

from application.routes import (
    redirect,
    http_response,
    current_user,
)

from utils import (
    log,
    template,
)


def welcome(request):
    """
    显示欢迎页面
    """
    body = template('user/welcome.html')
    return http_response(body)


def login(request):
    """
    处理登录请求
    """
    form = request.form()
    u = User(form)
    if u.validate_login():
        session_id = Session.new(u)
        headers = {
            'Set-Cookie': 'session_id={}; Path=/'.format(session_id)
        }
        return redirect('/twitter/twitter/index', headers)
    else:
        return redirect('/twitter/user/welcome')


def register(request):
    """
    处理注册请求
    """
    form = request.form()
    u = User.new(form)
    if u.validate_register:
        u.save()
    return redirect('/twitter/user/welcome')
