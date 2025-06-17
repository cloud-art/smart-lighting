from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    # MQTT
    MQTT_BROKER: str
    MQTT_PORT: int
    MQTT_USER: str
    MQTT_PASS: str
    MQTT_KEEPALIVE: int

    # DB
    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: str

    @property
    def DATABASE_URL(self) -> PostgresDsn:  # noqa: C0103
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    # Redis/Celery
    REDIS_HOST: str
    REDIS_PORT: str

    @property
    def CELERY_BROKER_URL(self) -> RedisDsn:  # noqa: C0103
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    # ML
    MODEL_PATH: str


settings = Settings()
