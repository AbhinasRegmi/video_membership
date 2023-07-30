from typing import Optional

from pydantic import EmailStr

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from membership.core.config import settings
from membership.exceptions.user import UserAlreadyExistError
from membership.utils.password import generate_pwd_hash, verify_pwd

class UserModel(Model):
    __keyspace__ = settings.CASSANDRA_DB_KEYSPACE

    email = columns.Text(primary_key=True)
    hpassword = columns.Text()

    def __repr__(self):
        return f"UserModel(email={self.email})"
    

    @classmethod
    def create_user(cls, email: EmailStr, password: str) -> 'UserModel':
        user = UserModel.objects.filter(email=email).first()

        if user:
            raise UserAlreadyExistError
        
        hpwd = generate_pwd_hash(plain_pwd=password)
        return UserModel.objects.create(email=email, hpassword=hpwd)

    @classmethod
    def get_user_with_validation(cls, email: EmailStr, password: str) -> Optional['UserModel']:
        """
        Get user that matches the email and password.
        """
        user = UserModel.objects.filter(email=email).first()
        if not user:
            return None
        
        if not verify_pwd(password, user.hpassword):
            return None
        
        return user
    
    @classmethod
    def get_user_by_email(cls, email: EmailStr) -> Optional['UserModel']:
        return UserModel.objects.filter(email=email).first()