from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Server Configuration
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # WhatsApp Cloud API Configuration
    WHATSAPP_VERIFY_TOKEN: str = "my_secure_verify_token_123"
    WHATSAPP_API_TOKEN: str = "your_whatsapp_api_token_here"
    WHATSAPP_PHONE_NUMBER_ID: str = "your_whatsapp_phone_number_id_here"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
