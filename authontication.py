from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def get_hashed_password(password: str) -> str:
    # Ensure string and truncate to 72 bytes
    password = str(password)[:72]
    return pwd_context.hash(password)
