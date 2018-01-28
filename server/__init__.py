import socket
import _thread
import pkgutil
import os
import inspect

import application.routes
from application.routes import (
    error,
    login_required,
)

from server.request import Request

from utils import log


def all_route_modules():
    """
    获取 routes 文件夹下，除 __init__.py 所有的模块
    返回由模块组成的列表
    """
    package_path = os.path.dirname('./application/routes/__init__.py')
    package_name = os.path.basename(package_path)
    
    route_modules = []
    # 列出目录下所有模块的模块名
    for _, file, _ in pkgutil.iter_modules([package_path]):
        r = eval('application.' + package_name + '.' + file)
        route_modules.append(r)
    
    return route_modules


def routes_dict_for_file(file):
    """
    举例：
    对于 api_comment.py 中的 all 函数，生成 '/twitter/comment/all' -> all 的映射
    """
    parts = file.__name__.split('_')
    if parts[1] == 'static':
        prefix = '/twitter'
    else:
        prefix = '/twitter/{}'.format(parts[1])
    
    routes_dict = {}
    # functions 是 file 中所有函数组成的列表
    functions = inspect.getmembers(file, inspect.isfunction)
    for r in functions:
        # r 是一个 tuple: (文件名, 函数实现)
        # inspect.getmodule 返回函数定义所在的模块
        module_of_func = inspect.getmodule(r[1])
        # 如果该函数定义于该文件
        if module_of_func == file:
            name = r[0].replace('_', '/')
            url = '{}/{}'.format(prefix, name)
            # 建立映射
            routes_dict[url] = r[1]
    
    return routes_dict


def routes_dict_for_modules(route_modules):
    rd = {}
    for m in route_modules:
        r = routes_dict_for_file(m)
        rd.update(r)
    return rd


def add_login_validation(routes_dict):
    rd = routes_dict
    
    exceptional_routes = [
        '/twitter/static',
        '/twitter/user/login',
        '/twitter/user/welcome',
        '/twitter/user/register',
        '/twitter/twitter/index',
    ]
    
    for k, v in rd.items():
        if k not in exceptional_routes:
            rd[k] = login_required(v)


def log_routes_dict(routes_dict):
    rd = '\n------------- routes -------------\n'
    for p, r in routes_dict.items():
        rd += '{}: {}\n'.format(p, r)
    rd += '------------- end -------------'
    log(rd)


def response_for_path(request):
    route_modules = all_route_modules()
    routes_dict = routes_dict_for_modules(route_modules)
    
    add_login_validation(routes_dict)
    
    log_routes_dict(routes_dict)
    
    if request.path[:15] == '/twitter/static':
        response = routes_dict.get('/twitter/static')
    else:
        response = routes_dict.get(request.path, error)
    
    return response(request)


def recv_request(connection):
    r = b''
    buffer_size = 1024
    while True:
        _r = connection.recv(buffer_size)
        r += _r
        if len(r) < buffer_size:
            break
    r = r.decode()
    return r


def log_response(request, response):
    if '/static' in request.path:
        log("static resource | size of response for static: {}".format(len(response)))
    else:
        log("response:\n{}".format(response.decode()))


def process_request(connection):
    """
    处理请求，发送响应
    """
    r = recv_request(connection)
    request = Request(r)
    log('request.cookies in process_request', request.cookies)
    response = response_for_path(request)
    log_response(request, response)
    
    connection.sendall(response)
    connection.close()


def run(host, port):
    """
    根据配置，启动服务器
    """
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        log('开始运行，host: {}，port: {}\nTest address：http://localhost:{}/twitter/twitter/index'.format(host, port, port))
        s.listen()
        while True:
            connection, address = s.accept()
            # 多线程：一次请求，一个线程
            _thread.start_new_thread(process_request, (connection,))
