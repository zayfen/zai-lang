"""Tests for zai.config module."""

import json
import tempfile
from pathlib import Path

import pytest

from zai.config import Config, get, get_bool, get_config, get_float, get_int, get_str


class TestConfig:
    """Test suite for Config class."""

    @pytest.fixture(autouse=True)
    def reset_config(self):
        """Reset Config singleton before each test."""
        Config.reset_instance()
        yield
        Config.reset_instance()
        # Re-create instance after reset to avoid None issues
        Config()

    @pytest.fixture
    def temp_dir(self):
        """Provide a temporary directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_config_singleton(self):
        """Test that Config is a singleton."""
        config1 = Config()
        config2 = Config()
        assert config1 is config2

    def test_get_from_env_var(self, temp_dir, monkeypatch):
        """Test reading from environment variables."""
        monkeypatch.setenv("ZAI_MODEL", "gpt-4")
        monkeypatch.setenv("ZAI_TIMEOUT", "30")

        config = Config(str(temp_dir))
        assert config.get("ZAI_MODEL") == "gpt-4"
        assert config.get("ZAI_TIMEOUT") == "30"

    def test_get_from_local_config(self, temp_dir):
        """Test reading from local .zai/config.json."""
        zai_dir = temp_dir / ".zai"
        zai_dir.mkdir()
        config_file = zai_dir / "config.json"
        config_file.write_text(json.dumps({"ZAI_MODEL": "claude-3", "ZAI_TIMEOUT": 60}))

        config = Config(str(temp_dir))
        assert config.get("ZAI_MODEL") == "claude-3"
        assert config.get("ZAI_TIMEOUT") == 60

    def test_get_from_user_config(self, temp_dir, monkeypatch):
        """Test reading from ~/.config/zai/config.json."""
        home_dir = temp_dir / "home"
        home_dir.mkdir()
        config_dir = home_dir / ".config" / "zai"
        config_dir.mkdir(parents=True)
        config_file = config_dir / "config.json"
        config_file.write_text(json.dumps({"ZAI_API_KEY": "user-key", "ZAI_MODEL": "gpt-3.5"}))

        monkeypatch.setattr(Path, "home", lambda: home_dir)
        monkeypatch.setattr(Path, "cwd", lambda: temp_dir)

        config = Config(str(temp_dir))
        assert config.get("ZAI_API_KEY") == "user-key"
        assert config.get("ZAI_MODEL") == "gpt-3.5"

    def test_precedence_env_over_local(self, temp_dir, monkeypatch):
        """Test that env vars override local config."""
        monkeypatch.setenv("ZAI_MODEL", "env-model")

        zai_dir = temp_dir / ".zai"
        zai_dir.mkdir()
        config_file = zai_dir / "config.json"
        config_file.write_text(json.dumps({"ZAI_MODEL": "local-model"}))

        config = Config(str(temp_dir))
        assert config.get("ZAI_MODEL") == "env-model"

    def test_precedence_local_over_user(self, temp_dir, monkeypatch):
        """Test that local config overrides user config."""
        home_dir = temp_dir / "home"
        home_dir.mkdir()
        config_dir = home_dir / ".config" / "zai"
        config_dir.mkdir(parents=True)
        user_config = config_dir / "config.json"
        user_config.write_text(json.dumps({"ZAI_MODEL": "user-model"}))

        zai_dir = temp_dir / ".zai"
        zai_dir.mkdir()
        local_config = zai_dir / "config.json"
        local_config.write_text(json.dumps({"ZAI_MODEL": "local-model"}))

        monkeypatch.setattr(Path, "home", lambda: home_dir)

        config = Config(str(temp_dir))
        assert config.get("ZAI_MODEL") == "local-model"

    def test_get_default(self, temp_dir):
        """Test default value when key not found."""
        config = Config(str(temp_dir))
        assert config.get("ZAI_NONEXISTENT") is None
        assert config.get("ZAI_NONEXISTENT", "default") == "default"

    def test_get_str(self, temp_dir, monkeypatch):
        """Test get_str method."""
        monkeypatch.setenv("ZAI_VAR", "test-value")
        config = Config(str(temp_dir))
        assert config.get_str("ZAI_VAR") == "test-value"
        assert config.get_str("ZAI_MISSING", "default") == "default"

    def test_get_int(self, temp_dir, monkeypatch):
        """Test get_int method."""
        monkeypatch.setenv("ZAI_TIMEOUT", "30")
        config = Config(str(temp_dir))
        assert config.get_int("ZAI_TIMEOUT") == 30
        assert config.get_int("ZAI_MISSING", 10) == 10

    def test_get_int_invalid(self, temp_dir, monkeypatch):
        """Test get_int with invalid value."""
        monkeypatch.setenv("ZAI_TIMEOUT", "invalid")
        config = Config(str(temp_dir))
        assert config.get_int("ZAI_TIMEOUT", 10) == 10

    def test_get_bool(self, temp_dir, monkeypatch):
        """Test get_bool method."""
        config = Config(str(temp_dir))

        for value in ["true", "1", "yes", "on", "TRUE"]:
            monkeypatch.setenv("ZAI_FLAG", value)
            Config.reset_instance()
            config = Config(str(temp_dir))
            assert config.get_bool("ZAI_FLAG") is True

    def test_get_bool_false(self, temp_dir, monkeypatch):
        """Test get_bool with false values."""
        config = Config(str(temp_dir))

        for value in ["false", "0", "no", "off", "FALSE"]:
            monkeypatch.setenv("ZAI_FLAG", value)
            Config.reset_instance()
            config = Config(str(temp_dir))
            assert config.get_bool("ZAI_FLAG") is False

    def test_get_float(self, temp_dir, monkeypatch):
        """Test get_float method."""
        monkeypatch.setenv("ZAI_TEMPERATURE", "0.7")
        config = Config(str(temp_dir))
        assert config.get_float("ZAI_TEMPERATURE") == 0.7
        assert config.get_float("ZAI_MISSING", 1.0) == 1.0

    def test_get_all(self, temp_dir, monkeypatch):
        """Test get_all method."""
        monkeypatch.setenv("ZAI_MODEL", "gpt-4")

        zai_dir = temp_dir / ".zai"
        zai_dir.mkdir()
        local_config = zai_dir / "config.json"
        local_config.write_text(json.dumps({"ZAI_TIMEOUT": 30}))

        config = Config(str(temp_dir))
        all_config = config.get_all()

        assert all_config["ZAI_MODEL"] == "gpt-4"
        assert all_config["ZAI_TIMEOUT"] == 30

    def test_reload(self, temp_dir, monkeypatch):
        """Test reload method."""
        monkeypatch.setenv("ZAI_MODEL", "initial")
        config = Config(str(temp_dir))
        assert config.get("ZAI_MODEL") == "initial"

        monkeypatch.setenv("ZAI_MODEL", "updated")
        config.reload()
        assert config.get("ZAI_MODEL") == "updated"

    def test_missing_config_files(self, temp_dir):
        """Test handling of missing config files."""
        config = Config(str(temp_dir))
        assert config.get("ZAI_ANYTHING") is None

    def test_empty_config_file(self, temp_dir, monkeypatch):
        """Test handling of empty config file."""
        # Clear environment to ensure isolation
        monkeypatch.delenv("ZAI_MODEL", raising=False)
        monkeypatch.delenv("ZAI_BASE_URL", raising=False)
        Config.reset_instance()

        zai_dir = temp_dir / ".zai"
        zai_dir.mkdir()
        config_file = zai_dir / "config.json"
        config_file.write_text("")

        config = Config(str(temp_dir))
        assert config.get("ZAI_TEST_VAR") is None

    def test_invalid_json(self, temp_dir, monkeypatch):
        """Test handling of invalid JSON."""
        # Clear environment to ensure isolation
        monkeypatch.delenv("ZAI_MODEL", raising=False)
        monkeypatch.delenv("ZAI_BASE_URL", raising=False)
        Config.reset_instance()

        zai_dir = temp_dir / ".zai"
        zai_dir.mkdir()
        config_file = zai_dir / "config.json"
        config_file.write_text("not valid json")

        config = Config(str(temp_dir))
        assert config.get("ZAI_TEST_VAR") is None

    def test_key_must_start_with_zai(self, temp_dir):
        """Test that keys must start with ZAI_ and be uppercase."""
        config = Config(str(temp_dir))
        with pytest.raises(ValueError, match="key must be uppercase and start with ZAI_"):
            config.get("MODEL")
        with pytest.raises(ValueError, match="key must be uppercase and start with ZAI_"):
            config.get("model")
        with pytest.raises(ValueError, match="key must be uppercase and start with ZAI_"):
            config.get("ZAI_model")


class TestModuleFunctions:
    """Test module-level convenience functions."""

    @pytest.fixture(autouse=True)
    def reset_config(self):
        """Reset Config singleton before each test."""
        Config.reset_instance()
        yield
        Config.reset_instance()
        # Re-create instance after reset to avoid None issues
        Config()

    @pytest.fixture
    def temp_dir(self):
        """Provide a temporary directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_get_config(self, temp_dir, monkeypatch):
        """Test get_config function."""
        monkeypatch.setattr(Path, "cwd", lambda: temp_dir)
        config = get_config()
        assert isinstance(config, Config)

    def test_module_get(self, monkeypatch):
        """Test module-level get function."""
        monkeypatch.setenv("ZAI_MODEL", "test-model")
        Config.reset_instance()
        assert get("ZAI_MODEL") == "test-model"

    def test_module_get_str(self, monkeypatch):
        """Test module-level get_str function."""
        monkeypatch.setenv("ZAI_VAR", "test")
        Config.reset_instance()
        assert get_str("ZAI_VAR") == "test"

    def test_module_get_int(self, monkeypatch):
        """Test module-level get_int function."""
        monkeypatch.setenv("ZAI_NUM", "42")
        Config.reset_instance()
        assert get_int("ZAI_NUM") == 42

    def test_module_get_bool(self, monkeypatch):
        """Test module-level get_bool function."""
        monkeypatch.setenv("ZAI_FLAG", "true")
        Config.reset_instance()
        assert get_bool("ZAI_FLAG") is True

    def test_module_get_float(self, monkeypatch):
        """Test module-level get_float function."""
        monkeypatch.setenv("ZAI_TEMP", "0.5")
        Config.reset_instance()
        assert get_float("ZAI_TEMP") == 0.5

    def test_module_key_must_start_with_zai(self):
        """Test that module-level functions require ZAI_ prefix and uppercase."""
        with pytest.raises(ValueError, match="key must be uppercase and start with ZAI_"):
            get("MODEL")
        with pytest.raises(ValueError, match="key must be uppercase and start with ZAI_"):
            get_str("model")
        with pytest.raises(ValueError, match="key must be uppercase and start with ZAI_"):
            get_int("timeout")
        with pytest.raises(ValueError, match="key must be uppercase and start with ZAI_"):
            get_bool("flag")
        with pytest.raises(ValueError, match="key must be uppercase and start with ZAI_"):
            get_float("temp")
