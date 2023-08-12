from pathlib import Path
from typing import List, Union

from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips

from src.logger import logger
from src.utils import Elem


def get_stock_videos(folder: Union[str, Path]) -> List[Union[str, Path]]:
    """
    Get a list of stock videos from the specified folder.

    :param folder: The folder path (str or Path object) containing the stock videos.
    :return: An ordered list of file paths (str or Path objects) representing the stock videos.
    """
    return sorted(
        (path for path in Path(folder).iterdir() if path.suffix == ".mp4"),
        key=lambda p: tuple(map(int, p.stem.split("_"))),
    )


def get_audio(folder: Union[str, Path]) -> str:
    """
    Retrieve the path of the audio file with the extension '.wav' from the specified folder.

    :param folder: The folder path to search for the audio file. Can be a string or a Path object.
    :return: The path of the audio file (as a string) found in the folder.
    """
    return [str(item) for item in Path(folder).iterdir() if item.suffix == ".wav"][0]


def make_video(
    elements: List[Elem],
    audio_path: str,
    video_paths: List[Union[str, Path]],
    output_path: Union[str, Path],
) -> None:
    """
    Create a video by combining elements, audio, and video clips.

    :param elements: A list of elements representing the structure of the video.
    :param audio_path: The path to the audio file to be used in the video.
    :param video_paths: A list of video paths to be included in the video.
    :param output_path: The path where the final video will be saved.

    :return: None
    """
    logger.info("Assembling video...")
    # Load audio clip
    audio = AudioFileClip(audio_path)
    # Calculate duration for each paragraph
    durations = [
        item.percent * audio.duration for item in elements if item.type == "text"
    ]

    final_clips = []
    for paragraph_n, paragraph_duration in enumerate(durations):
        paragraph_clips = []
        videos = [
            VideoFileClip(str(path))
            for path in video_paths
            if int(path.stem.split("_")[0]) == paragraph_n
        ]
        for video in videos:
            # if remainder paragraph_duration <= duration of next video,
            # cut it to paragraph_duration remainder
            if paragraph_duration <= video.duration:
                video.set_duration(paragraph_duration)
            paragraph_clips.append(video)
            paragraph_duration -= video.duration
            if paragraph_duration <= 0:
                break

        paragraph_clip = concatenate_videoclips(paragraph_clips, method="compose")
        final_clips.append(paragraph_clip)

    final_clip = concatenate_videoclips(final_clips, method="compose")

    # Set audio for the final clip
    final_clip = final_clip.set_audio(audio)

    # Write the final video file
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=30)
