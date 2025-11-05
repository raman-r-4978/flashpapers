"""Tests for configuration management."""

import json

import pytest

from flashpapers.config import ConfigManager
from flashpapers.models import AppConfig


class TestConfigManager:
    """Tests for ConfigManager class."""

    def test_load_default_config(self, config_manager):
        """Test loading default configuration."""
        config = config_manager.load()

        assert isinstance(config, AppConfig)
        assert config.backup_frequency_days == 7
        assert config.current_user == "default"
        assert len(config.categories) > 0

    def test_save_config(self, config_manager, temp_dir):
        """Test saving configuration."""
        config = config_manager.load()
        config.backup_frequency_days = 14

        config_manager._config = config
        config_manager.save()

        # Verify file was created
        assert config_manager.config_path.exists()

        # Load and verify
        with open(config_manager.config_path, "r") as f:
            data = json.load(f)

        assert data["backup_frequency_days"] == 14

    def test_update_config(self, config_manager):
        """Test updating configuration values."""
        config_manager.update(backup_frequency_days=21, current_user="test_user")

        config = config_manager.get_config()
        assert config.backup_frequency_days == 21
        assert config.current_user == "test_user"

    def test_update_categories(self, config_manager):
        """Test updating categories."""
        new_categories = ["Category A", "Category B", "Category C"]
        config_manager.update(categories=new_categories)

        config = config_manager.get_config()
        assert config.categories == new_categories

    def test_reset_to_defaults(self, config_manager):
        """Test resetting configuration to defaults."""
        # Modify config
        config_manager.update(backup_frequency_days=99, current_user="custom")

        # Reset
        config_manager.reset_to_defaults()

        config = config_manager.get_config()
        assert config.backup_frequency_days == 7
        assert config.current_user == "default"

    def test_load_existing_config(self, temp_dir):
        """Test loading an existing configuration file."""
        config_path = temp_dir / "existing_config.json"

        # Create a config file
        config_data = {
            "categories": ["Custom Category"],
            "backup_frequency_days": 10,
            "last_backup_timestamp": None,
            "srs_parameters": {
                "initial_ease_factor": 2.5,
                "minimum_interval_days": 1,
                "maximum_interval_days": 365,
                "easy_bonus": 1.3,
                "hard_penalty": 0.8,
            },
            "current_user": "existing_user",
            "data_directory": "data",
        }

        with open(config_path, "w") as f:
            json.dump(config_data, f)

        # Load it
        manager = ConfigManager(config_path=config_path)
        config = manager.load()

        assert config.categories == ["Custom Category"]
        assert config.backup_frequency_days == 10
        assert config.current_user == "existing_user"

    def test_config_persistence(self, config_manager):
        """Test that config persists across instances."""
        # Update config
        config_manager.update(backup_frequency_days=30)

        # Create new instance with same path
        new_manager = ConfigManager(config_path=config_manager.config_path)
        config = new_manager.load()

        assert config.backup_frequency_days == 30

    def test_invalid_update(self, config_manager):
        """Test updating with invalid field."""
        # Should not raise error, just ignore invalid fields
        config_manager.update(invalid_field="value")

        config = config_manager.get_config()
        assert not hasattr(config, "invalid_field")
