from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    @staticmethod
    def bcrypt(password: str) -> str:
        """Genera un hash para la contraseña."""
        return pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        """Verifica si la contraseña en texto plano coincide con el hash."""
        return pwd_context.verify(plain_password, hashed_password)