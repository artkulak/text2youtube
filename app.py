from pathlib import Path

from src.audio import generate_voice_over
from src.config import cfg
from src.logger import logger
from src.openai_generation import run_openai_generation
from src.utils import (
    generate_video_meta,
    get_cookies,
    get_source_files,
    prep_directories,
    read_data_from_file,
    split_openai_output,
)
from src.video import get_audio, get_stock_videos, make_video
from src.video_processing import save_videos

cookies = get_cookies()


def run(file_path: Path):
    # read data from txt file
    input_data: str = read_data_from_file(file_path)
    logger.info("Input data loaded")
    # run openai prompt with file
    openai_output = ""
    for _ in range(3):
        cur_output = run_openai_generation(input_data, "prompt.txt")
        cur_output = cur_output.replace('"', "").replace("'", "")
        if len(cur_output.split()) > len(openai_output.split()):
            openai_output = cur_output
        if len(openai_output.split()) >= 500:
            break
    logger.info("OpenAI response received")
    # split data into pieces
    splitted_output = split_openai_output(openai_output)

    file_output_dir = f"{cfg.PROCESS_DIR}/{file_path.stem}"
    # save video metadata into folder
    generate_video_meta(splitted_output, file_output_dir)

    # generate audio
    audio_duration = generate_voice_over(splitted_output, file_output_dir)

    # save videos for further use
    save_videos(splitted_output, audio_duration, file_output_dir, cookies, cfg.YT_PROBA)

    # generate video
    # make_video(
    #     splitted_output,
    #     get_audio(file_output_dir),
    #     get_stock_videos(f"{file_output_dir}/videos"),
    #     f"{OUTPUT_DIR}/{file_path.stem}.mp4",
    # )


def main():
    logger.info("App start")
    prep_directories()
    for file_path in get_source_files(cfg.SOURCE_DIR):
        logger.info(f"Processing: {file_path}")
        run_completed = False
        while not run_completed:
            # try:
            run(file_path)
            run_completed = True
            # except Exception as e:
            #     print("Failed on file ", file_path, " with exception ", e)


if __name__ == "__main__":
    main()
