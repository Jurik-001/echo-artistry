"""Generate a blog post from a YouTube video."""

import argparse
import os

from tqdm import tqdm

from echo_artistry.src import utils
from echo_artistry.src.transcriber import Transcriber
from echo_artistry.src.comic_story_generator import ComicStoryGenerator
from echo_artistry.src.cost_management import CostManager


def args_call():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate stunning art stories based on your voice message.",
    )
    #TODO decide if it is cooler to have  it as argument or as input
    parser.add_argument(
        "audio_path",
        type=str,
        help="The path to the audio file.",
    )
    parser.add_argument(
        "output_dir",
        type=str,
        help="The directory to save the summary file.",
    )
    parser.add_argument("api_key",
                        type=str,
                        help="The API key for openai API.",
                        )
    parser.add_argument(
        "--model_name",
        type=str,
        default="gpt-3.5-turbo-1106",
        help="The model name used as blog generator.",
    )
    args = parser.parse_args()
    main(args.audio_path, args.output_dir, args.api_key, args.model_name)

def main(audio_path, output_dir, api_key, model_name):
    """Download, transcribe, and generate comics from a voice memo.

    Args:
        audio_path (str): The path to the audio file.
        output_dir (str): The directory to save the summary file.
        api_key (str): The API key for openai API.
        model_name (str): The model name used as blog generator.
    """
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    cost_manager = CostManager(model_name=model_name)
    transcriber = Transcriber(output_path=output_dir)
    comic_story_generator = ComicStoryGenerator(model_name)

    tasks = ["Transcribing Audio", "Generating Comic Story", "Generating Comic"]

    with tqdm(total=len(tasks)) as pbar:

        transcription = transcriber.transcribe_audio(audio_path)
        pbar.update(1)
        comic_story = comic_story_generator.generate_story(transcription)
        pbar.update(1)





if __name__ == "__main__":
    args_call()
