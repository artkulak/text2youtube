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
    @patch(
        "src.config.safe_load",
        return_value=conf_dict,
    )
    def test_get_config_with_custom_path(self, mock_safe_load):
        custom_path = "custom_path.yaml"
        config = get_config(custom_path)
        mock_safe_load.assert_called_once()
        assert config == Config(
            OPENAI_API_KEY="your_key",
            OPENAI_PROMPTS_PATH="path",
            SOURCE_DIR="source",
            PROCESS_DIR="process",
            OUTPUT_DIR="output",
            YT_PROBA=80,
        )
