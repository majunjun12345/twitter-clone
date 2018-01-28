from application.models import Model
from application.models.user import User
import time


class Comment(Model):
    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)
        self.twitter_id = int(form.get('twitter_id', -1))
    
    @classmethod
    def new(cls, form, user_id):
        m = super().new(form)
        m.user_id = user_id
        m.save()
        return m
    
    @classmethod
    def update(cls, id, form):
        t = cls.find(id)
        valid_names = [
            'content',
        ]
        for key in form:
            if key in valid_names:
                setattr(t, key, form[key])
        t.updated_time = int(time.time())
        t.save()
        return t
    
    def user(self):
        u = User.find_by(id=self.user_id)
        return u
