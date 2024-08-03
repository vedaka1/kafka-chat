import os


class SMTPConfig:
    SMTP_PASSWORD: str = os.environ.get("SMTP_PASSWORD")
    SMTP_HOST: str = os.environ.get("SMTP_HOST")
    SMTP_PORT: int = int(os.environ.get("SMTP_PORT", default=465))
    SMTP_EMAIL: str = os.environ.get("SMTP_EMAIL")
    SMTP_SUBJECT: str = os.environ.get("SMTP_SUBJECT")


class Config:
    SMTP = SMTPConfig()
    KAFKA_URL: str = os.environ.get("KAFKA_URL", default="kafka:29092")


settings = Config()
