from dataclasses import dataclass

@dataclass(frozen=True)
class AppConfig:
    aes_key_auth: str
    aes_key_user: str
    jwt_user_key: str