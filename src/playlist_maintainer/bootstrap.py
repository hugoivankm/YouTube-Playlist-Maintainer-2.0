import os
import tomllib
import pathlib
import shutil
from dotenv import load_dotenv
from playlist_maintainer.app_config import get_app_config


_app_initialized = False
def initialize_app(env_file_name: str = None):
    """
    Initializes the core application environment, allowing specification of a .env file.
    This function should be called by all application entry points (CLI, GUI, Web).
    Determines environment precedence: Application interface(e.g CLI '--env') arg > Custom '.env' (specified in the configuration
    file) > APP_ENV env var
    Args:
        env_filename (str, optional): The specific .env file to load (e.g., "prod.env", "qa.env").
                                      If None, load_dotenv() will search for ".env" by default
                                      in the current directory and its parents.
    """
    global _app_initialized
    if _app_initialized:
        print(
            "INFO: Application already initialized. Skipping redundant initialization."
        )
        return
    
    if not env_file_name:
        try:
            home_dir = pathlib.Path(os.path.expanduser("~"))
            ytpl_dir_path = pathlib.Path(os.path.join(home_dir, 'ytpl'))
            full_ytpl_file_path = pathlib.Path(os.path.join(ytpl_dir_path))
            default_settings_path = pathlib.Path(os.path.join(os.getcwd(), 'configs', 'defaults', 'settings.toml'))
            
            MAX_RETRIES = 2
            retries = 0
            has_settings_file = True if (os.path.isfile(full_ytpl_file_path / 'settings.toml')) else False
            if has_settings_file:
                print(f"Settings file already exists: {full_ytpl_file_path}")
            while not has_settings_file and retries < MAX_RETRIES:
                if os.path.exists(ytpl_dir_path):
                    print(f"ytpl settings directory: {ytpl_dir_path}")
                    if os.path.isfile(full_ytpl_file_path):
                        has_settings_file = True
                        print(f"Settings file available in: {full_ytpl_file_path}")
                    else:
                        retries+=1
                        if _setup_settings_file(default_settings_path, full_ytpl_file_path):
                            has_settings_file = True   
                else:
                    retries += 1
                    if _setup_settings_file(default_settings_path, full_ytpl_file_path):
                        has_settings_file = True
            env_file_name = f"{full_ytpl_file_path / 'settings.toml'}"              
        except Exception as e:
            print(f"Unable to create settings file at: {full_ytpl_file_path} please check permissions")
            print(f"Error: {e}")    
    
    try:
        settings = None
        YTPL_CONFIG_DIR = os.path.expanduser('~/ytpl')
        with open(f"{YTPL_CONFIG_DIR}/settings.toml", 'rb') as f:
            settings = tomllib.load(f)
        
        env: str | None = settings.get("Environment", {}).get('env', None)
        
        if env:
            if not env.endswith(".env"):
                env = env.strip()
                env += ".env"
            load_dotenv(f"./configs/{env}")
            get_app_config(env, settings)
        else:
            print("No env specified, falling back to environment variables previous created by user.")
            
    except FileNotFoundError:
        print("Error: The config.toml file was not found.")
    except tomllib.TOMLDecodeError:
        print("Error: Failed to parse the TOML file. Check its syntax.")
    except Exception as e:
        print(f"Unexpected error: {e}")   
        
def _setup_settings_file(default_settings_path: pathlib.Path, settings_destination: pathlib.Path):
    """
    Creates a directory structure for the destination and copies a file
    from a default source path to that destination.
    
    Args:
        default_path (pathlib.Path): Path for the default settings in ytpl.
        settings_destination (pathlib.Path): Path for the settings file in the user home directory.
        
    Returns:
        bool: True if the file successfully copied, False otherwise.
    """
    try:
        if not os.path.exists(settings_destination):
            os.makedirs(settings_destination, exist_ok=True)
            print(f"Setting directory structure successfully created at: {settings_destination}")
        else:
            print(f"Setting directory already exists: {settings_destination}")
            
        if not os.path.exists(default_settings_path):
            print(f"Error: Default source path not found at '{default_settings_path.parent}'")
            return False
        if not os.path.isfile(default_settings_path):
            print(f"Error: Default source file '{default_settings_path}' is not a file.")
            return False
        
        shutil.copy2(default_settings_path, settings_destination)
        print(f"Successfully copied '{default_settings_path}' to '{settings_destination}'")
        return True
        
    except Exception as e:
        print("Unable to create ytpl settings files")
        print(f"Error: {e}")
        return False


    


