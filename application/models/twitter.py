from application.models import Model
from application.models.comment import Comment


class Twitter(Model):
    """
    微博类
    """
    
    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', user_id)
    
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
        t.save()
        return t
    
    def owner(self, id):
        return self.user_id == id
    
    def comments(self):
        return Comment.find_all(twitter_id=self.id)
