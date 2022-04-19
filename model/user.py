from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, user_json):
        if("email" in user_json):
            self.email = user_json['email']
        else:
            self.email = ""
            self.is_anonymous = True
        self.name = user_json['name']
        self.password = user_json['password']
        self.user_json = user_json

    def get_id(self):
        object_id = self.user_json.get('email')
        return str(object_id)

    def __str__(self):
        user = """
        'email': %s, 
        'name': %s, 
        'is_active': %s,
        'is_authenticated': %s
        """ % (self.email, self.name, str(self.is_active), str(self.is_authenticated))

        return user
