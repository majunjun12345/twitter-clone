import time
import json

from utils.micro_template import MicroTemplate


def formatted_time(unixtime):
    dt = time.localtime(unixtime)
    ds = time.strftime('%Y-%m-%d %H:%M:%S', dt)
    return ds


def create_log_file(time_string, *args, **kwargs):
    date = time_string[:10]
    ts = time_string[11:]
    
    file_name = 'logs/{}.log'.format(date)
    with open(file_name, 'a', encoding='utf-8') as f:
        print(ts, *args, file=f, **kwargs)


def log(*args, **kwargs):
    unixtime = int(time.time())
    ds = formatted_time(unixtime)
    print(ds, *args, **kwargs)
    
    create_log_file(ds, *args, **kwargs)


def template(path, **kwargs):
    path = 'application/views/templates/{}'.format(path)
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
    t = MicroTemplate(s)
    return t.render(**kwargs)


def save(data, path):
    """
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load', s)
        return json.loads(s)
