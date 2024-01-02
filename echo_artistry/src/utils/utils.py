"""This module provides utility functions."""

import logging

import tiktoken

logging.basicConfig(filename='echo_artistry.log', level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
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
            "1024×1024": 0.020,
            "512x512": 0.018,
            "256x256": 0.016,

        }
    }
}

DEFAULT_MODEL_NAME = "gpt-3.5-turbo-1106"


def save_to_md_file(content, file_path):
    """Save content to a markdown file.

    Args:
        content (str): The content to save.
        file_path (str): The path to the file to save to.

    Returns:
        str: The path to the saved file.
    """
    with open(file_path, "w") as f:
        f.write(content)
    logging.info(f"Blog post saved to: {file_path}")
    return file_path


def format_to_markdown(text):
    """Format text to markdown.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    lines = text.split("\\n")

    formatted_lines = []

    for line in lines:
        if line.startswith("#"):
            if formatted_lines:
                formatted_lines.append("")
        formatted_lines.append(line)

    formatted_text = "\n".join(formatted_lines)

    return formatted_text


class TokenCounter:
    """A class for counting tokens."""

    def __init__(self, model_name=DEFAULT_MODEL_NAME):
        self.encoding = tiktoken.encoding_for_model(model_name)
        self.model_token_length = MODEL_TOKEN_LENGTH_MAPPING[model_name]["token_length"]

    def count_tokens(self, text):
        """Count the number of tokens in a text.

        Args:
            text (str): The text to count the tokens of.

        Returns:
            int: The number of tokens in the text.
        """
        token_count = len(self.encoding.encode(text))
        return token_count
