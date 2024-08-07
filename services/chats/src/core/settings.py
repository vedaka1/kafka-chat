from src.utils.common import get_env_var


class DatabaseSettings:
    POSTGRES_HOST: str = get_env_var("POSTGRES_HOST", to_cast=str, default="postgres")
    POSTGRES_PORT: int = get_env_var("POSTGRES_PORT", to_cast=int, default=5432)
    POSTGRES_USER: str = get_env_var("POSTGRES_USER", to_cast=str)
    POSTGRES_PASSWORD: str = get_env_var("POSTGRES_PASSWORD", to_cast=str)
    POSTGRES_DB: str = get_env_var("POSTGRES_DB", to_cast=str)

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class Settings:
    db: DatabaseSettings = DatabaseSettings()


settings = Settings()
