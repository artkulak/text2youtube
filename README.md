<p>
<img src="https://img.shields.io/github/forks/artkulak/text2youtube.svg">
<img src="https://img.shields.io/github/stars/artkulak/text2youtube.svg">
<img src="https://img.shields.io/github/watchers/artkulak/text2youtube.svg">
<img src="https://img.shields.io/github/last-commit/artkulak/text2youtube.svg">
<img src="https://hits.sh/github.com/artkulak/text2youtube.svg">
</p>

# 🎬 text2youtube

## Description

text2youtube leverages the power of AI to automate the process of video content creation. This project aims to streamline the creation of engaging videos by employing advanced AI technologies for scenario generation, text-to-speech synthesis, and video compilation.

## Features

📜 Automated video script generation from prompt + reference information (like from another video script). We not only generate the script itself but also queries to Youtube/Storyblocks so that we can compose our video later from a set of clips we download from those queries.

🎙 Video voice generation with Bark. Bark is the best for naturally sounding voice at the moment, voice is one of the most important parts of a Youtube video and we did a bunch of experiments there. It runs quick on Google Colab with A100 GPU attached. 

🎨 We have some basic code for stitching videos together with MoviePY but it works real slow, so for now we just export the clips from Storyblocks/Youtube and voice-over and stitch them together in Adobe Premier which takes seconds not minutes.

## Demos

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1NpBJ4CFtGK4PWxQkb9D6pD5a2KNf8eKt?usp=sharing)


## Getting Started

1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Install text-to-speech `pip install git+https://github.com/suno-ai/bark.git`
3. Ensure the `cookies.json` file is present with necessary credentials for **storyblocks.com** website access.
4. Ensure `env.yaml` file is present providing OpenAi API key and working directories
5. Provide the necessary OpenAI prompt in prompts directory
6. Provide the necessary content inputs in text files in SOURCE_DIR
7. Run the main application file `app.py` to start the content creation process.
8. The program will handle the rest, creating engaging videos with captivating voiceovers.

## Project Structure

The project is organized into several modules:

- `src.audio`: Contains audio-related functions for text-to-speech synthesis.
- `src.config`: Stores configuration settings for the program.
- `src.logger`: Implements logging functionality for the application.
- `src.openai_generation`: Handles interactions with OpenAI's ChatGPT for scenario generation.
- `src.video_processing`: Manages video downloads from YouTube or videoblocks.com.
- `src.utils`: Contains utility functions for data processing and file handling.
- `src.video`: Includes video-related functions for compilation and editing.

## Results

While developing, we decided to focus on the finance niche and create a youtube channel on Economics/Countries topic. [Here is the channel](https://www.youtube.com/channel/UC0JQ0xmoK_lcg5AchMGmI4Q)

We posted 1 video daily for about 20-25 days. In the end, we got around 8,000 views, 221 watch hours, and +70 subscribers, average watch time of the video was around 30%. The results of the experiment are pretty encouraging because the videos are not of very high quality and I expected worse.


## What To Improve
- It's hard to change the quality of naturally sounding voice generation at the moment but I think we can have a big boost in video generation itself. For example, finding a way to make high-quality text overlays on top of video clips would give a big advantage. Or parsing images from google and applying parallax (ken burns effect) on top
- Improving video generation speed with MoviePY, so videos wouldn't have to be exported into adobe premier pro.
- Allow option to create youtube shorts content, though there are plenty projects which already do that.

## Dependencies

- [OpenAI GPT-3 API](https://openai.com): For scenario generation using language models.
- [Neural Network Text-to-Speech Library BARK](https://github.com/suno-ai/bark/): For realistic audio synthesis.
- [Python Requests Library](https://pypi.org/project/requests/): For website access and video downloads.
- [MoviePy Library](https://pypi.org/project/moviepy/): For video compilation and editing.


## Contributors

- [Art Kulakov](https://github.com/artkulak)
- [Movses M](https://github.com/mirmozavr)


## License

This project is licensed under the [MIT License](LICENSE). Feel free to use and modify it according to your needs.

[![Test and lint](https://github.com/artkulak/text2youtube/actions/workflows/check.yml/badge.svg)](https://github.com/artkulak/text2youtube/actions/workflows/check.yml)
