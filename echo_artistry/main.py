"""Generate a blog post from a YouTube video."""

import argparse
import os

from tqdm import tqdm

from echo_artistry.generators import (
    ComicImageGenerator,
    ComicStoryGenerator,
    FileNameGenerator,
)
from echo_artistry.services import CostManager, TokenCounter, Transcriber
from echo_artistry.utils import OpenAIClient, helper


def args_call():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate stunning art stories based on your voice message.",
    )
    parser.add_argument(
        "audio_path",
        type=str,
        help="The path to the audio file.",
    )
    parser.add_argument(
        "output_path",
        type=str,
        help="The directory to save the summary file.",
    )
    parser.add_argument(
        "api_key",
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
    main(args.audio_path, args.output_path, args.api_key, args.model_name)


def main(audio_path, output_path, api_key, model_name):
    """Download, transcribe, and generate comics from a voice memo.

    Args:
    ----
        audio_path (str): The path to the audio file.
        output_path (str): The directory to save the summary file.
        api_key (str): The API key for openai API.
        model_name (str): The model name used as blog generator.
    """
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    token_counter = TokenCounter(model_name=model_name)
    cost_manager = CostManager(token_counter, model_name=model_name)
    client = OpenAIClient(cost_manager, model_name=model_name)
    transcriber = Transcriber(output_path=output_path)
    file_name_generator = FileNameGenerator(client)
    comic_story_generator = ComicStoryGenerator(client, output_path=output_path)
    comic_image_generator = ComicImageGenerator(client, output_path=output_path)

    tasks = [
        "Transcribing audio",
        "Generate file name",
        "Generating comic story",
        "Generating comic",
    ]

    with tqdm(total=len(tasks)) as pbar:
        transcription = transcriber.transcribe_audio(audio_path)
        pbar.update(1)
        file_name = file_name_generator.generate_file_name(transcription)
        pbar.update(1)
        comic_file_name = f"{file_name}.txt"
        comic_story = comic_story_generator.generate_story(
            transcription,
            file_name=comic_file_name,
        )
        pbar.update(1)
        comic_image_file_name = f"{file_name}.png"
        comic_image_generator.generate_image(comic_story, file_name=comic_image_file_name)
        pbar.update(1)

        total_cost = cost_manager.get_total_cost()
        helper.logging.info(f"Comic is generated.\nTotal cost: {total_cost} USD")


if __name__ == "__main__":
    args_call()
