from dataclasses import dataclass
from http.client import HTTPException
from pathlib import Path
from random import randint, sample
from typing import Union

from requests import get

from src.logger import logger
from src.utils import Elem
from src.yt_download import download_yt_video

STORYBLOCKS_BASE_URL = "https://www.storyblocks.com"
STORYBLOCKS_SEARCH_URL = f"{STORYBLOCKS_BASE_URL}/api/video/search"


@dataclass
class Video:
    title: str
    duration: int
    url: str


def get_storyblocks_video_urls(
    search_terms: list[str], n_results: int, cookies: dict
) -> list[Video]:
    query_n_results = max(n_results, 10)
    params = {
        "categories": "",
        "templateType": "",
        "searchTerm": "-".join(search_terms),
        "video_quality": "HD",
        "sort": "most_relevant",
        "page": 1,
        "results_per_page": query_n_results,
        "load-more": "false",
        "search-origin": "search_bar",
        "min_duration": 5,
        "max_duration": 60,
        "has_talent_released": "",
        "has_property_released": "",
    }
    response = get(STORYBLOCKS_SEARCH_URL, params=params, cookies=cookies)
    if response.status_code != 200:
        raise HTTPException(f"Bad status code {response.status_code}")

    n_results = min(n_results, len(response.json()["data"]["stockItems"]))

    return sample(
        [
            Video(
                item["stockItem"]["title"],
                int(item["stockItem"]["duration"]),
                f'{STORYBLOCKS_BASE_URL}{item["stockItemFormats"][-1]["downloadUrl"]}',
            )
            for item in response.json()["data"]["stockItems"]
        ],
        n_results,
    )


def save_videos(
    elements: list[Elem],
    total_duration: float,
    file_output_dir: Union[str, Path],
    cookies: dict,
    yt_proba: int,
) -> None:
    """
    Save videos based on the provided `elements` and their durations.

    :param elements: A list of `Elem` objects representing the elements.
    :param total_duration: The total duration in seconds.
    :param file_output_dir: The directory where the videos will be saved.
    :param cookies: A `CookieJar` object containing the necessary cookies for authentication.
    :param yt_proba: Probability to use YouTube as a video source in percent

    :return: None
    """
    logger.info("Start video collection...")
    queries = [item.text for item in elements if item.type == "query"]
    durations = [
        item.percent * total_duration for item in elements if item.type == "text"
    ]
    for n_paragraph, (query, duration) in enumerate(zip(queries, durations)):
        if randint(0, 100) <= yt_proba:
            download_yt_video(duration, file_output_dir, n_paragraph, query)
        else:
            save_storyblocks(cookies, duration, file_output_dir, n_paragraph, query)


def save_storyblocks(
    cookies: dict,
    duration: Union[int, float],
    file_output_dir: str,
    n_paragraph: int,
    query: str,
) -> None:
    """
    Save videos from Storyblocks or fallback to saving from YouTube.

    :param cookies: The cookies required for Storyblocks authentication.
    :type cookies: dict
    :param duration: The desired total duration in seconds.
    :type duration: int
    :param file_output_dir: The directory where the videos will be saved.
    :type file_output_dir: str
    :param n_paragraph: The paragraph number.
    :type n_paragraph: int
    :param query: The search query for videos.
    :type query: str
    :return: None
    """
    videos: list[Video] = get_storyblocks_video_urls(
        query.split(), int(duration / 5), cookies
    )
    if not videos:
        download_yt_video(duration, file_output_dir, n_paragraph, query)
        return
    # drop less relevant videos from the end, if sum duration is enough without them
    while (
        len(videos) > 1
        and sum((video.duration for video in videos)) - videos[-1].duration > duration
    ):
        videos.pop()
    # iterate through urls and save them in video folder
    for v_num, url in enumerate((video.url for video in videos)):
        v_path = f"{file_output_dir}/videos/{n_paragraph}_{v_num}.mp4"
        download_storyblocks_video(url, cookies, v_path)


def download_storyblocks_video(url: str, cookies: dict, path: Union[str, Path]) -> None:
    """
    Downloads a video from the specified URL using the provided cookies and saves it to the given file path.

    :param url: The URL of the video to download.
    :type url: str
    :param cookies: A dictionary containing cookies required for authentication, if needed.
    :type cookies: dict
    :param path: The path where the downloaded video will be saved.
    :type path: Union[Path, str]
    :return: None
    """
    response = get(url, cookies=cookies)
    if response.status_code != 200:
        raise HTTPException(f"Bad status code {response.status_code}")

    with open(path, "wb") as file:
        file.write(response.content)
