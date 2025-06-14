import os

class AppConfig:
    """
    Manages application configuration instances. It assumes the environment is correctly initialized.
    """
    def __init__(self, env_file_name: str | None, settings: dict = {}  ):
        self.dotenv_filename = env_file_name
        self.settings = settings
        
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.youtube_api_key:
            raise ValueError(
                "YOUTUBE_API_KEY environment variable is not set. Please ensure it's in your environment file or system environment."
            )

    _app_config_instance = None
    @classmethod
    def get_app_config(cls, dotenv_filename: str | None, settings: dict = {}):
        """
        Return the application configuration instance, loading if not already loaded.
        """
        cls._app_config_instance
        if cls._app_config_instance is None:
            cls._app_config_instance = AppConfig(dotenv_filename, settings)
        elif dotenv_filename is None:
            return cls._app_config_instance
        elif cls._app_config_instance.dotenv_filename != dotenv_filename:
            print(f"Loading new .env file for application configuration: {dotenv_filename}")
            cls._app_config_instance = AppConfig(dotenv_filename, settings)
        else:
            print(f"{cls._app_config_instance.dotenv_filename} already in use. Skipping initialization...")
        return cls._app_config_instance

    @classmethod
    def reset_app_config(cls):
       cls._app_config_instance = None