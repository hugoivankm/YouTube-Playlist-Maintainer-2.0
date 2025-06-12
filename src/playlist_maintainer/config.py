import os

class AppConfig:
    """
    Manages application configuration instances. It assumes the environment is correctly initialized.
    """
    def __init__(self, env_file_name: str = ".env"):
        self.dotenv_filename = env_file_name
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.youtube_api_key:
            raise ValueError(
                "YOUTUBE_API_KEY environment variable is not set. Please ensure it's in your environment file or system environment."
            )

_app_config_instance: AppConfig | None = None

def get_app_config(dotenv_filename: str) -> AppConfig:
    """
    Return the application configuration instance, loading if not already loaded.
    """
    global _app_config_instance
    if _app_config_instance is None:
        _app_config_instance = AppConfig(dotenv_filename)
    elif _app_config_instance.dotenv_filename != dotenv_filename:
        print(f"Loading new .env file for application configuration: {dotenv_filename}")
        _app_config_instance = AppConfig(dotenv_filename)
    else:
        print(f"{_app_config_instance.dotenv_filename} already in use. Skipping initialization...")
    return _app_config_instance
