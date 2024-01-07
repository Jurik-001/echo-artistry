"""helper module provides utility functions and constants."""

import logging

import tiktoken

logging.basicConfig(
    filename="echo_artistry.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger()

MODEL_TOKEN_LENGTH_MAPPING = {
    "gpt-3.5-turbo-1106": {
        "token_length": 16385,
        "input_token_cost": 0.0010,
        "output_token_cost": 0.0020,
    },
    "gpt-4-1106-preview": {
        "token_length": 128000,
        "input_token_cost": 0.01,
        "output_token_cost": 0.03,
    },
    "gpt-4": {
        "token_length": 8192,
        "input_token_cost": 0.03,
        "output_token_cost": 0.06,
    },
    "gpt-4-32k": {
        "token_length": 32768,
        "input_token_cost": 0.06,
        "output_token_cost": 0.12,
    },
}

IMAGE_CHARACTER_LENGTH_MAPPING = {
    "dall-e-2": {
        "character_length": 1000,
        "cost_per_image": {
            "standard": {
                "1024x1024": 0.020,
                "512x512": 0.018,
                "256x256": 0.016,
            },
        },
    },
    "dall-e-3": {
        "character_length": 4000,
        "cost_per_image": {
            "standard": {
                "1024x1024": 0.040,
                "1024x1792": 0.080,
                "1792x1024": 0.080,
            },
            "hd": {
                "1024x1024": 0.080,
                "1024x1792": 0.120,
                "1792x1024": 0.120,
            },
        },
    },
}

DEFAULT_MODEL_NAME = "gpt-3.5-turbo-1106"
DEFAULT_IMAGE_MODEL_NAME = "dall-e-3"
DEFAULT_IMAGE_SIZE = "1792x1024"
DEFAULT_IMAGE_QUALITY = "standard"
MAX_RETRIES = 5


def write_text_to_file(text, file_path):
    """Write text to a file.

    Args:
        text (str): The text to write.
        file_path (str): The path to the file.
    """
    with open(file_path, "w") as file:
        file.write(text)


def get_text_from_file(file_path):
    """Get the text from a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The text from the file.
    """
    with open(file_path, "r") as file:
        text = file.read()
    return text
