import nltk
import numpy as np
import soundfile as sf
from bark import SAMPLE_RATE
from bark.api import semantic_to_waveform
from bark.generation import generate_text_semantic, preload_models

from src.logger import logger

nltk.download("punkt")


def generate_voice_over(splitted_output: list, output_dir: str) -> float:
    """
    Generate voice-over audio from the given `splitted_output` and save it as a WAV file.

    :param splitted_output: A list of items representing the splitted output.
    :param output_dir: The output directory where the voice-over WAV file will be saved.
    :return: The duration of the generated voice-over audio in frames.
    """
    logger.info("Generate voiceover")
    preload_models()
    output_text = " ".join(
        (item.text for item in splitted_output if item.type == "text")
    )
    sentences = nltk.sent_tokenize(output_text)

    GEN_TEMP = 0.7
    SPEAKER = "v2/en_speaker_2"
    silence = np.zeros(int(0.25 * SAMPLE_RATE))  # quarter second of silence
    pieces = []
    for sentence in sentences:
        semantic_tokens = generate_text_semantic(
            sentence,
            history_prompt=SPEAKER,
            temp=GEN_TEMP,
            min_eos_p=0.05,  # this controls how likely the generation is to end
        )

        audio_array = semantic_to_waveform(
            semantic_tokens,
            history_prompt=SPEAKER,
        )
        pieces += [audio_array, silence.copy()]
    output = np.concatenate(pieces)
    file_path = f"{output_dir}/voiceover.wav"
    sf.write(file_path, output, SAMPLE_RATE)
    logger.info(f"Voice over saved OK {file_path}")
    # calculate duration
    temp = sf.SoundFile(file_path)
    return temp.frames / temp.samplerate
