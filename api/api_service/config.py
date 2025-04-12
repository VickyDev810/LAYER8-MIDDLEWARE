import os
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """API service settings with environment variable fallbacks."""
    
    # Server settings
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    # Configuration paths
    CONFIG_PATH: str = Field(default="config.json", env="CONFIG_PATH")
    MAPPINGS_FILE: str = Field(default="anonymizer_state.json", env="MAPPINGS_FILE")
    
    # NLP model settings
    SPACY_MODEL: str = Field(default="en_core_web_lg", env="SPACY_MODEL")
    
    # LLM API keys
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: str = Field(default="", env="ANTHROPIC_API_KEY")
    GEMINI_API_KEY: str = Field(default="", env="GEMINI_API_KEY")
    
    # Default LLM settings
    DEFAULT_PROVIDER: str = Field(default="gemini", env="DEFAULT_PROVIDER")
    DEFAULT_MODEL: str = Field(default="", env="DEFAULT_MODEL")
    DEFAULT_TEMPERATURE: float = Field(default=0.7, env="DEFAULT_TEMPERATURE")
    DEFAULT_MAX_TOKENS: int = Field(default=1000, env="DEFAULT_MAX_TOKENS")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore"  # Allow extra fields in env file
    }

# Create global settings instance
settings = Settings() 