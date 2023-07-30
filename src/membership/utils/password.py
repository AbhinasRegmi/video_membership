from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def generate_pwd_hash(plain_pwd: str) -> str:
    "Generate hashed password from plain password"
    return pwd_context.hash(secret=plain_pwd)

def verify_pwd(plain_pwd: str, hash_pwd: str) -> bool:
    "Verify if plain password and the hash password matches."
    return pwd_context.verify(secret=plain_pwd, hash=hash_pwd)