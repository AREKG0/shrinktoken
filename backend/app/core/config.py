from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    LLMLINGUA_MODEL_NAME: str = 'microsoft/llmlingua-2-xlm-roberta-large-meetingbank'
    DEVICE_MAP: str = 'cpu'
    DEFAULT_COMPRESSION_MODE: str = 'balanced'
    LOG_LEVEL: str = 'INFO'
    MAX_MODEL_CALLS: int = 4
    MINIMUM_TOKEN_SAVINGS: int = 3
    MIN_COMPRESSIBLE_LENGTH: int = 20
    
    model_config = SettingsConfigDict(env_prefix='STP_')

settings = Settings()
