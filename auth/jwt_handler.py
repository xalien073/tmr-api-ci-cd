#auth/jwt handler
from pydantic_settings import BaseSettings
import time
from typing import Dict
from jose import jwt

class Settings(BaseSettings):
    #      database configurations
#     DATABASE_URL: Optional[str] = None

#      JWT
    secret_key: str = "secret"
    algorithm: str = "HS256"

    class Config:
        # env_file = ".env"
        from_attributes = True

def token_response(token: str):
    return token

secret_key = Settings().secret_key

def sign_jwt(user_id: str) -> Dict[str, str]:
    # Set the expiry time.
    payload = {"user_id": user_id, "expires": time.time() + 15552000}
    return token_response(jwt.encode(payload, secret_key, algorithm="HS256"))

def decode_jwt(token: str) -> dict:
    print(f'decoding token')
    decoded_token = jwt.decode(token.encode(), secret_key, algorithms=["HS256"])
    print(f'decoded_token is {decoded_token}')
    return decoded_token if decoded_token["expires"] >= time.time() else {}
