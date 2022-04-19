from database import helper
from werkzeug.security import generate_password_hash
import os

new_user = {'email': os.environ['EMAIL_ADMIN'],
            'name': os.environ['NAME_ADMIN'],
            'password': generate_password_hash(os.environ['PASSWORD_ADMIN'], method='sha256')
            }

print(new_user)

# add the new user to the database
user_id = helper.add('users', new_user)
print(user_id)