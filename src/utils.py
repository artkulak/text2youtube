import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from src.config import cfg
from src.logger import logger


@dataclass
class Elem:
    type: str
    text: str
    percent: Optional[float] = None


def split_openai_output(raw_text: str, sep: str = "###") -> list[Elem]:
    """
    Splits incoming text from LLMs into arrays of elements.

    :param raw_text: The scenario received from LLM.
    :param sep: The element separator used to split the text. Defaults to "###".
    :return: A list of Elem objects representing the split text.
    """
    arr = [item.strip() for item in raw_text.split(sep)]
    elements = []
    for item in arr:
        if item.startswith("TITLE:"):
            elements.append(Elem("title", item[7:]))
        elif item.startswith("TEXT:"):
            elements.append(Elem("text", item[6:]))
        elif item.startswith("QUERY:"):
            elements.append(Elem("query", item[7:]))
        elif item.startswith("DESCRIPTION:"):
            elements.append(Elem("description", item[13:]))

    total_text_len = sum((len(item.text) for item in elements if item.type == "text"))
    for element in elements:
        if element.type == "text":
            element.percent = len(element.text) / total_text_len

    return elements


def generate_video_meta(splitted_output: list, file_output_dir: str):
    logger.info("Generating video meta...")
    os.makedirs(f"{file_output_dir}/videos", exist_ok=True)

    meta = "\n\n".join(
        (item.text for item in splitted_output if item.type in ("title", "description"))
    )
    video_text = " ".join(
        (item.text for item in splitted_output if item.type == "text")
    )

    with open(f"{file_output_dir}/meta.txt", "w") as f:
        f.write(meta)

    with open(f"{file_output_dir}/video_text.txt", "w") as f:
        f.write(video_text)
    logger.info("Meta saved OK")


def read_data_from_file(input_path: Union[str, Path]) -> str:
    with open(input_path, "r", encoding="UTF-8") as f:
        input_data = f.read()
    return input_data


def get_source_files(source_dir: str) -> list[Path]:
    """
     Retrieves a list of source files with a '.txt' extension from the specified directory.
    :param source_dir: The directory path to search for source files.
    :return: list[str | Path]: A list of file paths (as strings or Path objects) to the found source files.
    """
    return [
        item for item in Path(source_dir).iterdir() if item.suffix.lower() == ".txt"
    ]


def get_cookies() -> dict:
    """
    Fetches browser cookies from the "cookies.json" file and returns them as a dictionary.

    :return: A dictionary containing browser cookies, with the cookie names as keys
    and their corresponding values as values.
    :rtype: dict
    """
    cookies = json.loads(open("cookies.json").read())
    logger.info("Cookies loaded OK")
    return {i["name"]: i["value"] for i in cookies}


def prep_directories() -> None:
    try:
        shutil.rmtree(cfg.PROCESS_DIR)
        shutil.rmtree(cfg.OUTPUT_DIR)
    except Exception as e:
        logger.error(e)
    os.makedirs(cfg.PROCESS_DIR, exist_ok=True)
    os.makedirs(Path(f"{cfg.OUTPUT_DIR}/videos/yt"), exist_ok=True)
    logger.info("Directories prepared")
