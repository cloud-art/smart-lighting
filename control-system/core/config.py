from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # MQTT
    MQTT_BROKER: str = "localhost"
    MQTT_PORT: int = 1883
    MQTT_USER: str = "default_user"
    MQTT_PASS: str = "0000"
    MQTT_KEEPALIVE: int = 60
    MQTT_RECEIVE_TOPIC: str = "devices/+/data"

    @property
    def CELERY_BROKER_URL(self) -> RedisDsn:  # noqa: C0103
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    # DB
    POSTGRES_HOST: str = "localhost"
    POSTGRES_DB: str = "iot_db"
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "0000"
    POSTGRES_PORT: str = "5432"

    @property
    def DATABASE_URL(self) -> PostgresDsn:  # noqa: C0103
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Redis/Celery
    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = "6379"

    # ML
    MODEL_PATH: str = "model.joblib"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
