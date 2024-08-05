import os


class DBConfig:
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST", default="postgres")
    POSTGRES_PORT: int = int(os.environ.get("POSTGRES_PORT", default="5432"))
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class JwtConfig:
    PRIVATE_KEY: str = os.environ.get("PRIVATE_KEY")
    PUBLIC_KEY: str = os.environ.get("PUBLIC_KEY")
    ALGORITHM: str = os.environ.get("ALGORITHM", default="RS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.environ.get("EXPIRATION_DELTA", default=5)
    )


class Config:
    KAFKA_URL: str = os.environ.get("KAFKA_URL", default="kafka:29092")

    db: DBConfig = DBConfig()
    jwt: JwtConfig = JwtConfig()


settings = Config()
