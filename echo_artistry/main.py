"""Generate a blog post from a YouTube video."""

import argparse
import os

from tqdm import tqdm

from echo_artistry.src import utils
from echo_artistry.src.transcriber import Transcriber


def args_call():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate stunning art stories based on your voice message.",
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
    main(args.output_dir, args.api_key, args.model_name)

def main(output_dir, api_key, model_name):
    """Download, transcribe, and generate blog post of a YouTube video.

    Args:
        output_dir (str): The directory to save the summary file.
        api_key (str): The API key for openai API.
        model_name (str): The model name used as blog generator.
    """
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    transcriber = Transcriber(output_path=output_dir)

    tasks = ["Transcribing Audio"]

    with tqdm(total=len(tasks)) as pbar:

        transcription_path = transcriber.transcribe_audio(audio_path)
        utils.logging.info(f"Audio transcribed to: {transcription_path}")
        pbar.update(1)


    utils.logging.info(f"Blog post cost: {cost_manager.get_total_cost()}$")


if __name__ == "__main__":
    args_call()
