from pydantic import BaseSettings
class Settings(BaseSettings):
    UPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_JWT_SECRET: str

    class Config:
        env_file = ".env"
settings = Settings()