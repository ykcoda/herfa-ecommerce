from fastapi.security import OAuth2PasswordBearer

OAUTH2_USER_SCHEMA = OAuth2PasswordBearer(tokenUrl="/api/users/token")
