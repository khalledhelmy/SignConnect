from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
    )

    # App Info
    APP_NAME: str
    APP_VERSION: str

    # Fine-tuned Whisper Model Settings
    BASE_MODEL: str
    MODEL_NAME: str
    HF_REPO: str

    # HuggingFace Authentication
    HF_TOKEN: str
    HF_CACHE_DIR: str
    
    #Fine-tuned tts Model Settings
    BASE_MODEL_tts : str
    VOCODER_MODEL_tts : str
    SPEAKER_INDEX : int

    # HuggingFace Authentication for tts
    HF_CACHE_DIR_tts : str
    HF_TOKEN_tts : str



settings = Settings()