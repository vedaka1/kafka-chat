from passlib.context import CryptContext

from src.application.common.password_hasher import BasePasswordHasher

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHasher(BasePasswordHasher):
    def hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify(self, password: str, hash: str) -> bool:
        return pwd_context.verify(password, hash)
