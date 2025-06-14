# YouTube Playlist Maintainer

A command-line tool to simplify the maintenance, viewing, and export of YouTube playlist information. This project features a layered configuration system, service-oriented architecture, and an interactive command-line interface. This is a work in progress, some bugs or inconsistencies are expected but all constructive feedback is appreciated.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [License](#license)

## Installation

This project uses Poetry for dependency management.
1. Clone the repository:
    ```
    git clone https://github.com/hugoivankm/YouTubePlaylistMaintainer2.git
    cd YouTubePlaylistMaintainer2
    ```

2. Install Poetry (if you don't have it):
    ```
    curl -sSL https://install.python-poetry.org | python -
    ```

3. Install project dependencies:

    ```
    poetry install
    ```
    This command will create a virtual environment (if one doesn't exist) and install all required packages, including your project itself in editable mode.

## Configuration
The application uses a multi-layered configuration system to determine settings, especially which .env file to load various settigs.

### YouTube Data API Key
You'll need a YouTube Data API v3 key to interact with the YouTube API.

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Navigate to "APIs & Services" > "Enabled APIs & services" and enable the YouTube Data API v3.
4. Go to "APIs & Services" > "Credentials" and create new credentials (API key).
5. Restrict your API key to prevent unauthorized use. Good practice is to restrict it by API (YouTube Data API v3) and potentially by IP address if you know where your script will run.

### .env Files
.env files are used to store sensitive information (like your YOUTUBE_API_KEY).

```
YOUTUBE_API_KEY="YOUR_DEV_YOUTUBE_API_KEY"
```
myEnv.env: An example for a myEnv environment.


### settings.toml specifies several custom settings
Currently a settings.toml file is created in the user's home directory ($HOME) the first time the application is run, currently this can be done only through the CLI
'$HOME/ytpl/settings.toml'

###### This value will be overridden by APP_ENV environment variable or the --env CLI flag.

### General application settings (examples)
log_level = "INFO"
default_fetch_limit = 25
Environment Precedence
The application determines which .env file to load based on the following hierarchy (highest priority first):

1. CLI Argument (--env): If you specify --env prod, it will try to load prod.env.
2. Environment Variable (APP_ENV): If APP_ENV=qa is set, it will try to load qa.env.
application.toml: If neither CLI nor APP_ENV is set, it defaults to the default_env_filename specified in application.toml (e.g., .env).

Usage
You can run the CLI commands using poetry run.

General Command Structure

```
poetry run ytpl [OPTIONS] COMMAND [ARGS]...
show Command
Displays details of a YouTube playlist.
```

### Show details for a playlist using a custom .env ("<user-home-directory>/ytpl/settings.toml")
```
poetry run ytpl show PLFgK_b9v5J3E9N4J4S5Q5Q5T5U5V5W5X5Y
```

### Show details using the 'my.env' file via APP_ENV environment variable
```
APP_ENV=my poetry run ytpl show PLFgK_b9v5J3E9N4J4S5Q5Q5T5U5V5W5X5Y
```

### Show details using the 'prod.env' file via CLI option (overrides APP_ENV)
```
poetry run ytpl --env prod show PLFgK_b9v5J3E9N4J4S5Q5Q5T5U5V5W5X5Y
```

### Show details with a custom limit
```
poetry run ytpl show PLFgK_b9v5J3E9N4J4S5Q5Q5T5U5V5W5X5Y --limit 20
```
export Command
Exports a YouTube playlist to a specified file format (e.g., TXT, PDF).

## License
This project is licensed under the MIT License. See the LICENSE file for details.
