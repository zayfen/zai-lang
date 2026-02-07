"""
ZAI environment variable configuration manager.

Manages ZAI_* environment variables with the following precedence:
1. Shell environment variables (bash/zsh)
2. Current directory .zai/config.json
3. User config ~/.config/zai/config.json
"""

import json
import os
from pathlib import Path
from typing import Any, Optional


class Config:
    """Configuration manager for ZAI_* environment variables."""

    _instance: Optional["Config"] = None
    _initialized: bool = False

    def __new__(cls, cwd: Optional[str] = None) -> "Config":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, cwd: Optional[str] = None):
        if Config._initialized:
            return

        self._cwd = Path(cwd) if cwd else Path.cwd()
        self._env_vars: dict[str, str] = {}
        self._local_config: dict[str, Any] = {}
        self._user_config: dict[str, Any] = {}

        self._load_all()
        Config._initialized = True

    def _load_all(self) -> None:
        """Load configuration from all sources in order of precedence."""
        self._load_user_config()
        self._load_local_config()
        self._load_env_vars()

    def _load_env_vars(self) -> None:
        """Load ZAI_* variables from shell environment."""
        for key, value in os.environ.items():
            if key.startswith("ZAI_"):
                self._env_vars[key] = value

    def _load_local_config(self) -> None:
        """Load configuration from current directory .zai/config.json."""
        local_path = self._cwd / ".zai" / "config.json"
        self._local_config = self._read_json_file(local_path)

    def _load_user_config(self) -> None:
        """Load configuration from ~/.config/zai/config.json."""
        home = Path.home()
        user_path = home / ".config" / "zai" / "config.json"
        self._user_config = self._read_json_file(user_path)

    def _read_json_file(self, path: Path) -> dict[str, Any]:
        """Safely read a JSON config file."""
        if not path.exists():
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except (json.JSONDecodeError, IOError):
            return {}

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.

        Precedence:
        1. ZAI_* environment variables
        2. Current directory .zai/config.json
        3. ~/.config/zai/config.json

        Args:
            key: The configuration key (e.g., "model", "timeout")
            default: Default value if key not found

        Returns:
            The configuration value or default
        """

        if not key.startswith("ZAI_") or not key.isupper():
            raise ValueError(f"key must be uppercase and start with ZAI_, got: {key}")
            
        # 1. Check environment variables (highest priority)
        if key in self._env_vars:
            return self._env_vars[key]

        # 2. Check local config
        if key in self._local_config:
            return self._local_config[key]

        # 3. Check user config
        if key in self._user_config:
            return self._user_config[key]

        return default

    def get_str(self, key: str, default: str = "") -> str:
        """Get configuration value as string."""
        value = self.get(key, default)
        return str(value) if value is not None else default

    def get_int(self, key: str, default: int = 0) -> int:
        """Get configuration value as integer."""
        value = self.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get configuration value as boolean."""
        value = self.get(key)
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        return str(value).lower() in ("true", "1", "yes", "on")

    def get_float(self, key: str, default: float = 0.0) -> float:
        """Get configuration value as float."""
        value = self.get(key)
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    def get_all(self) -> dict[str, Any]:
        """
        Get all configuration values merged from all sources.

        Returns:
            Dictionary of all config values (keys must start with ZAI_)
        """
        result = {}

        # Start with user config (lowest priority)
        # Config file keys should be ZAI_* format
        for key, value in self._user_config.items():
            key_upper = key.upper()
            if key_upper.startswith("ZAI_"):
                result[key_upper] = value

        # Merge local config
        for key, value in self._local_config.items():
            key_upper = key.upper()
            if key_upper.startswith("ZAI_"):
                result[key_upper] = value

        # Environment variables override everything
        result.update(self._env_vars)

        return result

    def reload(self) -> None:
        """Reload configuration from all sources."""
        self._env_vars.clear()
        self._local_config.clear()
        self._user_config.clear()
        self._load_all()

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (useful for testing)."""
        cls._instance = None
        cls._initialized = False


def get_config(cwd: Optional[str] = None) -> Config:
    """
    Get the global Config instance.

    Args:
        cwd: Optional working directory for loading local config

    Returns:
        Config instance
    """
    return Config(cwd)


# Convenience functions for direct access
def get(key: str, default: Any = None) -> Any:
    """Get a configuration value."""
    return get_config().get(key, default)


def get_str(key: str, default: str = "") -> str:
    """Get configuration value as string."""
    return get_config().get_str(key, default)


def get_int(key: str, default: int = 0) -> int:
    """Get configuration value as integer."""
    return get_config().get_int(key, default)


def get_bool(key: str, default: bool = False) -> bool:
    """Get configuration value as boolean."""
    return get_config().get_bool(key, default)


def get_float(key: str, default: float = 0.0) -> float:
    """Get configuration value as float."""
    return get_config().get_float(key, default)
