import json
import urllib.parse

from utils import log


class Request(object):
    def __init__(self, raw_data):
        log('raw_data', raw_data)
        
        self.body = ''
        self.headers = {}
        self.path = ''
        self.query = {}
        self.cookies = {}
        
        self._setup(raw_data)
    
    def _setup(self, raw_data):
        header, self.body = raw_data.split('\r\n\r\n', 1)
        h = header.split('\r\n')
        
        parts = h[0].split()
        self.method = parts[0]
        
        path = parts[1]
        self.parse_path(path)
        
        self.add_headers(h[1:])
        self.add_cookies()
        
        self._log_request()
    
    def _log_request(self):
        content = """
------------ request ------------
headers: <{}>
---
path: <{}>
---
query: <{}>
---
cookies: <{}>
---
body: <{}>
------------ end ------------""".format(
            self.headers,
            self.path,
            self.query,
            self.cookies,
            self.body
        )
        
        log(content)
    
    def add_headers(self, header):
        """
        将 header 中的字串组装成字典
        """
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v
    
    def add_cookies(self):
        """
        从 headers 抽取 cookie
        """
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=', 1)
                self.cookies[k] = v
    
    def parse_path(self, path):
        """
        处理 get 请求
        """
        index = path.find('?')
        if index == -1:
            self.path = path
            self.query = {}
        else:
            path, query_string = path.split('?', 1)
            self.path = path
            
            args = query_string.split('&')
            query = {}
            for arg in args:
                k, v = arg.split('=')
                k, v = urllib.parse.unquote_plus(k), urllib.parse.unquote_plus(v)
                query[k] = v
            self.query = query
    
    def form(self):
        """
        处理 post 请求，返回 dict
        """
        body = self.body
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            k, v = urllib.parse.unquote_plus(k), urllib.parse.unquote_plus(v)
            f[k] = v
        return f
    
    def json(self):
        """
        解析 body 中的 json 格式字符串
        """
        return json.loads(self.body)
