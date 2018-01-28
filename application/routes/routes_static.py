def static(request):
    """
    处理静态资源
    """
    p = 'application/views' + request.path[8:]
    with open(p, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\n\r\n'
        binary = header + f.read()
        return binary
