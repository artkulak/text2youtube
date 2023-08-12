from unittest.mock import patch

from src.audio import generate_voice_over
from src.utils import Elem


class TestGenerateVoiceOver:
    @patch("src.audio.preload_models")
    @patch("src.audio.generate_text_semantic")
    @patch("src.audio.semantic_to_waveform")
    @patch("src.audio.sf.write")
    @patch("src.audio.sf.SoundFile")
    @patch("nltk.sent_tokenize")
    def test_generate_voice_over(
        self,
        mock_sent_tokenize,
        mock_soundfile,
        mock_sf_write,
        mock_semantic_to_waveform,
        mock_generate_text_semantic,
        mock_preload_models,
    ):
        # Prepare mock behavior for the external dependencies
        mock_sent_tokenize.return_value = ["This is a sentence.", "Another sentence."]
        mock_soundfile_instance = mock_soundfile.return_value
        mock_soundfile_instance.frames = 1000
        mock_soundfile_instance.samplerate = 24000
        mock_semantic_to_waveform.return_value = [0.1, 0.1, 0.1]
        mock_generate_text_semantic.return_value = [
            "semantic_token_1",
            "semantic_token_2",
        ]

        # Run the function
        output_duration = generate_voice_over(
            [Elem("text", "Another sentence.")],
            "output_dir",
        )

        # Assertions
        assert mock_preload_models.called
        mock_sent_tokenize.assert_called_with("Another sentence.")
        mock_generate_text_semantic.assert_called_with(
            "Another sentence.",
            history_prompt="v2/en_speaker_2",
            temp=0.7,
            min_eos_p=0.05,
        )
        mock_semantic_to_waveform.assert_called_with(
            ["semantic_token_1", "semantic_token_2"],
            history_prompt="v2/en_speaker_2",
        )
        mock_sf_write.assert_called_once()
        assert output_duration == 1000 / 24000
