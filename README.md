[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/essence-extractor)](https://pepy.tech/project/essence-extractor)
![GitHub issues](https://img.shields.io/github/issues/Jurik-001/echo-artistry)
[![Python CI](https://github.com/Jurik-001/echo-artistry/actions/workflows/ci.yaml/badge.svg)](https://github.com/Jurik-001/echo-artistry/actions/workflows/ci.yaml)
[![Documentation](https://img.shields.io/badge/-Documentation-gray?logo=readthedocs&style=flat&logoWidth=20)](https://essenceextractor.readthedocs.io/en/latest/)

# EchoArtistry 🎨🔊

EchoArtistry is an innovative tool that transforms spoken words into captivating visual stories 🌟. It takes voice messages and transforms them into comics, offering a unique blend of audio-visual artistry. Dive into the world of automated storytelling with EchoArtistry!

## Limitations ⚠️
- Results may vary based on the clarity and content of the input audio.

## Requirements 🛠️
Before you get started, make sure you have the following installed on your machine:
- [FFmpeg](https://ffmpeg.org/download.html): A complete, cross-platform solution to record, convert, and stream audio and video.

## Installation 🖥️

```bash
pip install echo-artistry
```

## Usage 🚀

Start by recording a voice message. Then, run EchoArtistry with your audio file:

```bash
python echo-artistry "path_to_audio_file.wav" "output_directory" "YOUR_API_KEY"
```
- **path_to_audio_file.wav**: Path to your audio file.
- **output_directory**: Directory to save generated comics.
- **YOUR_API_KEY**: Your OpenAI API key.
- **--model_name** (optional): Specify the AI model, default is "gpt-3.5-turbo-1106".

## Output 🎁

EchoArtistry will create in your output directory:
- **Transcription File**: Text transcription of your audio.
- **Comic Story File (.txt)**: The narrative script of your comic.
- **Comic Image File (.png)**: The final comic strip.

## Documentation 📖
For more details on EchoArtistry's capabilities and how to use them, visit our [documentation](https://echoartistry.readthedocs.io/en/latest/).

## Join the EchoArtistry Community 🤝

We love collaboration and feedback! 🚀 If you have ideas or encounter any issues, please contribute. Check out our [contributing guidelines](https://github.com/yourusername/EchoArtistry/blob/master/.github/CONTRIBUTING.md) to get started.

## Roadmap 🗺️

Stay tuned for what's next in EchoArtistry's journey! Check out our [project roadmap](https://github.com/users/yourusername/projects/1) for upcoming features and enhancements. We're dedicated to improving EchoArtistry and expanding its storytelling capabilities.