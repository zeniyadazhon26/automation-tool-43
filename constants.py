from typing import Final, Dict, List, Any

# Configuration Constants for automation-tool-43

TIMEOUT_SECONDS: Final[int] = 30
MAX_RETRIES: Final[int] = 5

STATUS_CODES: Final[Dict[str, int]] = {
    "SUCCESS": 200,
    "REDIRECT": 302,
    "CLIENT_ERROR": 400,
    "SERVER_ERROR": 500
}

ALLOWED_EXTENSIONS: Final[List[str]] = [".json", ".yaml", ".yml", ".toml"]

def get_app_metadata() -> Dict[str, Any]:
    """
    Retrieve static metadata for the automation engine.

    Returns:
        Dict[str, Any]: A dictionary containing versioning and build info.
    """
    return {
        "version": "1.0.43",
        "env": "production",
        "engine": "auto-core-v2"
    }

class AppRegistry:
    """
    A container for globally accessed runtime constants.
    """
    REGISTRY_ID: Final[str] = "at-43-registry"
    DEFAULT_PATH: Final[str] = "/opt/automation/data"

    @classmethod
    def get_defaults(cls) -> List[str]:
        """
        Return essential registry configuration keys.

        Returns:
            List[str]: A list of base registry paths.
        """
        return [cls.DEFAULT_PATH, "/tmp/cache"]
