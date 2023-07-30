from membership.core.db import get_cdb
from membership.models.user import UserModel
from membership.exceptions.user import UserAlreadyExistError

DB = None
def test_connection():
    DB = get_cdb()
    print("db connected.")

def test_usercreation():
    try:
        user = UserModel.create_user(email="abhinas@gmail.com", password="abhinas12")
        print(user)
        print(user.email)
    except UserAlreadyExistError:
        print("user already exits")
    

def test_userq():
    user = UserModel.get_user(email="abhinas@gmail.com", password="abhinas12")
    print(user)
    print(user.email)
    print(user.hpassword)

if __name__ == "__main__":
    test_connection()
    test_usercreation()
    test_userq()