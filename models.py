from flask_login import UserMixin

class User(UserMixin):
    #username
    #password
    

    def check_admin(self):
        return self.username == " "