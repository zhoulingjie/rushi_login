from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "testpassword"
hashed_password = pwd_context.hash(password)
print(hashed_password)

verified = pwd_context.verify(password, hashed_password)
print(verified)