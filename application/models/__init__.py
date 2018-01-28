import json

from utils import (
    log,
    save,
    load,
)


class Model(object):
    def __init__(self, form):
        self.id = form.get('id', None)
    
    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'data/{}.json'.format(classname)
        return path
    
    @classmethod
    def _new_from_dict(cls, d):
        m = cls({})
        for k, v in d.items():
            setattr(m, k, v)
        return m
    
    @classmethod
    def all(cls):
        path = cls.db_path()
        models = load(path)
        ms = [cls._new_from_dict(m) for m in models]
        return ms
    
    @classmethod
    def new(cls, form):
        m = cls(form)
        return m
    
    @classmethod
    def find_by(cls, **kwargs):
        for m in cls.all():
            exist = False
            for key, value in kwargs.items():
                k, v = key, value
                if v == getattr(m, k):
                    exist = True
                else:
                    exist = False
            if exist:
                return m
        return None
    
    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)
    
    @classmethod
    def find_all(cls, **kwargs):
        models = []
        for m in cls.all():
            exist = False
            for key, value in kwargs.items():
                k, v = key, value
                if v == getattr(m, k):
                    exist = True
                else:
                    exist = False
            if exist:
                models.append(m)
        return models
    
    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)
    
    def save(self):
        models = self.all()
        
        first_index = 0
        if self.id is None:
            if len(models) > 0:
                self.id = models[-1].id + 1
            else:
                self.id = first_index
            models.append(self)
        else:
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self
        
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)
    
    @classmethod
    def delete(cls, id):
        models = cls.all()
        index = -1
        for i, e in enumerate(models):
            if e.id == id:
                index = i
                break
        if index != -1:
            o = models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            save(l, path)
            return o
    
    def json(self):
        d = self.__dict__
        return d
    
    @classmethod
    def all_json(cls):
        ms = cls.all()
        js = [t.json() for t in ms]
        return js
