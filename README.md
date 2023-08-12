# 🎬 text2youtube

## Description

The text2youtube is an innovative program that leverages the power of AI and neural networks to automate the process of video content creation. This project aims to streamline the creation of engaging videos by employing advanced AI technologies for scenario generation, text-to-speech synthesis, and video compilation.

## Features

🤖 Interacts with OpenAI's ChatGPT to take on various roles like a YouTuber or a YouTube channel.  
📜 Generates captivating video scenarios based on provided content or user inputs.  
🎙 Provides video meta information, including video descriptions and names, using ChatGPT.  
🔊 Utilizes neural network-based text-to-speech synthesis to create realistic and lifelike audio.  
🎨 Crafts compelling search queries for video backgrounds to complement the generated scenarios.  
🌐 Downloads suitable videos from YouTube or videoblocks.com based on the crafted search queries.  
✂ Cuts and edits the downloaded videos to synchronize with the synthesized voiceover.  

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

## Dependencies

- [OpenAI GPT-3 API](https://openai.com): For scenario generation using language models.
- [Neural Network Text-to-Speech Library BARK](https://github.com/suno-ai/bark/): For realistic audio synthesis.
- [Python Requests Library](https://pypi.org/project/requests/): For website access and video downloads.
- [MoviePy Library](https://pypi.org/project/moviepy/): For video compilation and editing.

## Contributors

- [Artyom K](https://github.com/artkulak)
- [Movses M](https://github.com/mirmozavr)


## License

This project is licensed under the [MIT License](LICENSE). Feel free to use and modify it according to your needs.

[![Test and lint](https://github.com/artkulak/text2youtube/actions/workflows/check.yml/badge.svg)](https://github.com/artkulak/text2youtube/actions/workflows/check.yml)