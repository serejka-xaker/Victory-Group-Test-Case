from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    db_echo: bool = False  

    model_config = SettingsConfigDict(
        env_file=".env",     
        extra="ignore",      
        case_sensitive=False 
    )

settings = Settings()
