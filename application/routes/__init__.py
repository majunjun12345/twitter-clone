import json
import os
import pkgutil

from application.models.session import Session
from application.models.user import User
from application.models.twitter import Twitter

from utils import log


def response_with_headers(headers=None, status_code=200):
    header = 'HTTP/1.1 {} OK\r\nContent-Type: text/html\r\n'
    header = header.format(status_code)
    if headers is not None:
        header += ''.join([
            '{}: {}\r\n'.format(k, v) for k, v in headers.items()
        ])
    return header


def http_response(body, headers=None):
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode()


def json_response(data):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
    body = json.dumps(data, ensure_ascii=False, indent=2)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def redirect(location, headers=None):
    h = {
        'Location': location
    }
    if headers is not None:
        h.update(headers)
    header = response_with_headers(h, 302)
    r = header + '\r\n' + ''
    return r.encode()


def error(code=404):
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def current_user(request):
    session_id = request.cookies.get('session_id', '')
    sessions = Session.all()
    for s in sessions:
        if s.session_id == session_id:
            u = User.find_by(id=s.user_id)
            return u
    return None


def login_required(route_function):
    def f(request):
        u = current_user(request)
        if u is None:
            return redirect('/twitter/user/welcome')
        else:
            return route_function(request)
    
    return f


def auto_import():
    package_path = os.path.dirname(__file__)
    package_name = os.path.basename(package_path)
    
    for _, file, _ in pkgutil.iter_modules([package_path]):
        __import__('application.' + package_name + '.' + file)


auto_import()
