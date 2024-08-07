from dataclasses import dataclass


@dataclass
class Token:
    access_token: str
    max_age: int
    # refresh_token: uuid.UUID
    token_type: str
