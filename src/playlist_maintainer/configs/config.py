import os
from dotenv import load_dotenv, find_dotenv

class AppConfig:
    """
    Manages application configuration, loading from environment variables.
    """
    def __init__(self, env_file_name : str = ".env"):
        dotenv_path = find_dotenv(env_file_name)

        if dotenv_path:
            load_dotenv(dotenv_path)
        # TODO: Implement a proper logging mechanism
            print(f"Succesfully load environment file from {dotenv_path}")
        else:
            print(f"Warning: .env file '{env_file_name}' not found, falling back to system environment variable")
    
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.youtube_api_key:
            raise ValueError("YOUTUBE_API_KEY environment variable is not set")



_app_config_instance = None

def get_app_config() -> AppConfig:
    """
    Return the application configuration instance, loading if not already loaded.
    """
    global _app_config_instance
    if _app_config_instance is None:
        _app_config_instance = AppConfig()
    return _app_config_instance
    
    
def load_environment_variables(env_file_name=".env"):
    """
    Loads environment variable from a specified .env file.
    By default, it looks for '.env' in the current directory and its parents.
    You can specify 'dev.env', 'prod.env' or similar for the respective environment.
    """
    dotenv_path = find_dotenv(env_file_name)

    if dotenv_path:
        load_dotenv(dotenv_path)
        # TODO: Implement a proper logging mechanism
        print(f"Succesfully load environment file from {dotenv_path}")
    else:
        print(f"Warning: .env file '{env_file_name}' not found, falling back to system environment variable")
    
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    if not YOUTUBE_API_KEY:
        raise ValueError("YOUTUBE_API_KEY environment variable is not set")

