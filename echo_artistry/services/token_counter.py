"""token_counter contains TokenCounter."""
import tiktoken

from echo_artistry import utils


class TokenCounter:
    """A class for counting tokens."""

    def __init__(self, model_name=utils.DEFAULT_MODEL_NAME):
        self.encoding = tiktoken.encoding_for_model(model_name)
        self.model_token_length = utils.MODEL_TOKEN_LENGTH_MAPPING[model_name][
            "token_length"
        ]

    def count_tokens(self, text):
        """Count the number of tokens in a text.

        Args:
            text (str): The text to count the tokens of.

        Returns:
            int: The number of tokens in the text.
        """
        token_count = len(self.encoding.encode(text))
        return token_count
