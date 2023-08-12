from pathlib import Path
from unittest.mock import patch

from src.config import Config, get_config

conf_dict = {
    "OPENAI_API_KEY": "your_key",
    "OPENAI_PROMPTS_PATH": "path",
    "SOURCE_DIR": "source",
    "PROCESS_DIR": "process",
    "OUTPUT_DIR": "output",
    "YT_PROBA": 80,
}


class TestConfigFunctions:
    @patch("builtins.open", create=True)
    @patch(
        "src.config.safe_load",
        return_value=conf_dict,
    )
    def test_get_config_with_custom_path(self, mock_safe_load, mock_open):
        custom_path = "custom_path.yaml"
        config = get_config(custom_path)
        assert config == Config(
            OPENAI_API_KEY="your_key",
            OPENAI_PROMPTS_PATH="path",
            SOURCE_DIR="source",
            PROCESS_DIR="process",
            OUTPUT_DIR="output",
            YT_PROBA=80,
        )
        mock_open.assert_called_once_with(custom_path, encoding="utf-8")
        mock_safe_load.assert_called_once()

    @patch("builtins.open", create=True)
    @patch(
        "src.config.safe_load",
        return_value=conf_dict,
    )
    def test_get_config_with_default_path(self, mock_safe_load, mock_open):
        default_path = Path(__file__).parent.parent.parent.joinpath("env.yaml")
        config = get_config()
        assert config == Config(
            OPENAI_API_KEY="your_key",
            OPENAI_PROMPTS_PATH="path",
            SOURCE_DIR="source",
            PROCESS_DIR="process",
            OUTPUT_DIR="output",
            YT_PROBA=80,
        )
        mock_open.assert_called_once_with(default_path, encoding="utf-8")
        mock_safe_load.assert_called_once()
