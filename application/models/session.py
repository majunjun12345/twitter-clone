import uuid

from application.models import Model
from application.models.user import User


class Session(Model):
    def __init__(self, form):
        super().__init__(form)
        self.session_id = form.get('session_id', '')
        self.user_id = form.get('user_id', '')
    
    @classmethod
    def new(cls, u):
        session_id = str(uuid.uuid4())
        u = User.find_by(username=u.username)
        form = dict(
            session_id=session_id,
            user_id=u.id,
        )
        m = super().new(form)
        m.save()
        return session_id
