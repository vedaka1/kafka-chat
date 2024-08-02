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


class Config:
    MODE: str = os.environ.get("MODE", default="DEV")

    db: DBConfig = DBConfig()


settings = Config()
