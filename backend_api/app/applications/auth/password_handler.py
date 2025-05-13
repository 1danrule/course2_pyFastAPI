from passlib.context import CryptContext


class PasswordEncrypt:

    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @classmethod
    async def get_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)