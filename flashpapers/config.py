"""Configuration management for Flashpapers application."""

import json
from pathlib import Path
from typing import Optional

from flashpapers.models import AppConfig


class ConfigManager:
    """Manages application configuration with file persistence."""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration manager.

        Args:
            config_path: Path to config file. Defaults to data/config.json
        """
        self.config_path = config_path or Path("data/config.json")
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self._config: Optional[AppConfig] = None

    def load(self) -> AppConfig:
        """
        Load configuration from file or create default.

        Returns:
            AppConfig instance
        """
        if self._config is not None:
            return self._config

        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._config = AppConfig(**data)
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                self._config = AppConfig()
        else:
            self._config = AppConfig()
            self.save()

        return self._config

    def save(self) -> None:
        """Save configuration to file."""
        if self._config is None:
            self._config = AppConfig()

        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self._config.model_dump(), f, indent=2, default=str)

    def update(self, **kwargs) -> None:
        """
        Update configuration values.

        Args:
            **kwargs: Configuration fields to update
        """
        config = self.load()
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        self.save()

    def get_config(self) -> AppConfig:
        """
        Get current configuration.

        Returns:
            AppConfig instance
        """
        return self.load()

    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        self._config = AppConfig()
        self.save()
