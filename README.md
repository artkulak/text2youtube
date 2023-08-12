[//]: (![text2youtube]&#40;https://your-project-image-url-here&#41;)
<div align="center">
  <img src="https://your-project-image-url-here" alt="Project Image">
</div>

# 🎬 text2youtube

## Description

Welcome to text2youtube! 🌟 This groundbreaking project harnesses the magic of AI and neural networks to revolutionize video content creation. Say goodbye to the tedious manual process – text2youtube takes care of scenario generation, text-to-speech synthesis, and video compilation with a sprinkle of AI innovation.

## Features

🤖 Step into various roles with ChatGPT, from YouTuber to YouTube channel owner.  
📜 Generate captivating video scenarios based on your content or inputs.  
🎙️ Craft video meta info, including names and descriptions, using the brilliance of ChatGPT.  
🔊 Experience the power of neural network-based text-to-speech synthesis for lifelike audio.  
🎨 Curate compelling search queries for stunning video backgrounds that complement your scenarios.  
🌐 Download fitting videos from YouTube or videoblocks.com, guided by your crafted search queries.  
✂️ Seamlessly cut and edit downloaded videos to sync up with the synthesized voiceover.  

## Getting Started

1. Start by installing the necessary dependencies: `pip install -r requirements.txt`.
2. Enhance your text-to-speech experience with: `pip install git+https://github.com/suno-ai/bark.git`.
3. Ensure `cookies.json` holds your **storyblocks.com** credentials for smooth access.
4. Keep things organized with `env.yaml`, providing your OpenAI API key and working directories.
5. Fill the prompts directory with essential OpenAI prompts.
6. Feed your creative juices by providing content inputs in text files within the `SOURCE_DIR`.
7. Fire up the creativity engine by running `app.py` – let it do the heavy lifting.
8. Relax and enjoy as the program crafts mesmerizing videos with captivating voiceovers.

## Project Structure

Dive into the modular organization of text2youtube:

- `src.audio`: Unleash audio magic with text-to-speech synthesis.
- `src.config`: Centralize configuration settings for the whole show.
- `src.logger`: Document the journey with built-in logging.
- `src.openai_generation`: Forge connections with ChatGPT for scenario creation.
- `src.video_processing`: Command video downloads from YouTube or videoblocks.com.
- `src.utils`: A treasure trove of utility functions for data and files.
- `src.video`: Unveil video mastery with compilation and editing.

## Dependencies

The brilliance behind the scenes:

- [OpenAI GPT-3 API](https://openai.com): Elevate scenarios with language model mastery.
- [Neural Network Text-to-Speech Library BARK](https://github.com/suno-ai/bark/): Elevate audio to lifelike realms.
- [Python Requests Library](https://pypi.org/project/requests/): Connect with the web for downloads and more.
- [MoviePy Library](https://pypi.org/project/moviepy/): Craft and edit videos with cinematic flair.

## Meet the Creators

Our fantastic minds behind text2youtube:

- [Artyom K](https://github.com/artkulak)
- [Movses M](https://github.com/mirmozavr)

## License

This project dances under the [MIT License](LICENSE). Go ahead, remix and enjoy!

[![Test and Lint](https://github.com/artkulak/text2youtube/actions/workflows/check.yml/badge.svg)](https://github.com/artkulak/text2youtube/actions/workflows/check.yml)
