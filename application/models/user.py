import hashlib

from application.models import Model

from config import salt


class User(Model):
    def __init__(self, form):
        super().__init__(form)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
    
    def save(self):
        self.password = self.salted_password(self.password)
        super().save()
    
    @staticmethod
    def salted_password(password):
        salted = password + salt
        h = hashlib.sha256(salted.encode('ascii')).hexdigest()
        return h
    
    def validate_login(self):
        u = User.find_by(username=self.username)
        if u is not None:
            return u.password == self.salted_password(self.password)
        else:
            return False
    
    def validate_register(self):
        u = User.find_by(username=self.username)
        valid = u is None and len(self.username) > 2 and len(self.password) > 2
        if valid:
            p = self.password
            self.password = self.salted_password(p)
            return True
        else:
            return False
