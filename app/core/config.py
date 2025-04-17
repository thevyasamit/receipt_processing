from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Receipt Processor"  # Name shown in documentation
    VERSION: str = "1.0.0"                    # API version


# Load settings from environment variables or defaults
settings = Settings() 