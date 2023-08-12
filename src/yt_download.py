import shutil
from pathlib import Path
from random import randint
from typing import Optional, Union

from moviepy.editor import VideoFileClip
from pytube import Search, Stream
from pytube.exceptions import VideoUnavailable

from src.logger import logger


def download_yt_video(duration, file_output_dir, n_paragraph, query) -> None:
    """
    Save video and clips from YouTube.

    :param duration: Paragraph duration.
    :param file_output_dir: The directory where the videos will be saved.
    :param n_paragraph Number of paragraph in process.
    :param query Search query.
    :return: None
    """
    # download full yt video for paragraph and get path to file
    v_path = _search_and_dl_yt_video(query, f"{file_output_dir}/videos/yt")
    n = int(duration // 7 + bool(duration % 7))
    # extract 7 sec clips
    get_clips(v_path, n, 7, file_output_dir, n_paragraph)


def _search_and_dl_yt_video(
    search_query: str, folder: Union[Path, str]
) -> Optional[str]:
    """
    Search for a YouTube video using the given query and download it.

    :param search_query: The query to search for on YouTube.
    :type search_query: str
    :param folder: The folder path where the video will be saved.
    :type folder: Union[Path, str]
    :returns Path to the saved video
    :rtype str
    """
    search = Search(search_query)
    if len(search.results) == 0:
        logger(f"No video found by query: {search_query}")
        return None

    # immediately add more videos
    search.get_next_results()
    for v in search.results:
        try:
            stream: Stream = v.streams.filter(
                adaptive=True, res="1080p", file_extension="mp4"
            ).first()
        except VideoUnavailable as e:
            logger.error(f"Error occurred at {v.title}: {e}")
            continue
        if stream:
            return stream.download(folder, f"{v.title}.mp4", "yt_")


def get_clips(
    path: str,
    n_clips: int,
    clips_duration: Union[int, float],
    output_folder: str,
    n_paragraph: int,
):
    """
    Extracts subclips from a video file based on the specified parameters.

    :param path: The path to the video file.
    :type path: str
    :param n_clips: The number of subclips to extract.
    :type n_clips: int
    :param clips_duration: The duration of each subclip in seconds.
    :type clips_duration: Union[int, float]
    :param output_folder: The path to the folder where the subclips will be saved.
    :type output_folder: str
    :param n_paragraph: Number of the paragraph to collect clips for.
    :type n_paragraph int
    """
    with VideoFileClip(path) as main_clip:
        if n_clips * clips_duration > main_clip.duration:
            logger.error(
                f"80% of main_clip duration {main_clip.duration} isn't enough for {n_clips} clips by {clips_duration} seconds"
            )
            return
        subclip_start_times = get_random_subclip_start_times(
            main_clip, n_clips, clips_duration
        )
        for i, t_start in enumerate(subclip_start_times):
            f_name = f"{output_folder}/videos/{n_paragraph}_{i}.mp4"
            with main_clip.subclip(t_start, t_start + clips_duration) as new_clip:
                new_clip: VideoFileClip
                new_clip.write_videofile(
                    f_name, codec="libx264", audio_codec="aac", fps=30
                )
                logger.info(f"FILE SAVED: {f_name}")
    try:
        shutil.rmtree(f"{output_folder}/videos/yt")
    except Exception:
        pass


def get_random_subclip_start_times(
    clip: VideoFileClip, n_clips: int, clips_duration: Union[int, float]
) -> list:
    """
    Generate a list of n random start times for subclips within the given video clip.

    :param clip: The VideoFileClip object representing the video from which subclips are generated.
    :type clip: VideoFileClip
    :param n_clips: The number of subclips to generate start times for.
    :type n_clips: int
    :param clips_duration: The duration in seconds of each subclip.
    :type clips_duration: Union[int, float]
    :return: A list of n integers representing the start seconds of the random subclips.
             If suitable subclip timings couldn't be found after a number of tries, an empty list is returned.
    :rtype: list

    :note: The function attempts to generate n random subclip start times within the video clip's duration,
           such that each subclip's duration is clips_duration. It will make up to 10,000 attempts to find
           suitable subclip timings. If successful, it returns a list of n integers representing the start
           seconds of the subclips. If not, an empty list is returned along with a message indicating that
           suitable subclip timings couldn't be found in the given number of tries.
    """
    number_of_tries = 10_000
    start, end = int(clip.duration * 0.1), int(clip.duration * 0.9 - clips_duration)
    for _ in range(number_of_tries):
        tup = sorted(randint(start, end) for _ in range(n_clips))
        if all([tup[i] + clips_duration <= tup[i + 1] for i in range(n_clips - 1)]):
            logger.info(f"Work with timings: {tup}")
            return tup
    else:
        logger.error(
            f"Somehow couldn't find suitable subclip timings in {number_of_tries} tries..."
        )
        return []
