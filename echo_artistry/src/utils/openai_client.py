"""OpenAI API client."""
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

MODEL_NAME = "gpt-3.5-turbo-1106"


class OpenAIError(Exception):
    """General error in OpenAI Client."""

    pass


class OpenAIClient:
    """OpenAI API client."""

    def __init__(self, model_name=MODEL_NAME):
        self.model_name = model_name
        self.client = OpenAI()

    def generate_answer(self, messages):
        """Generate answer.

        Args:
            messages (list(str)): List of messages.

        Returns:
            str: Generated answer.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise OpenAIError(f"An unexpected error occurred: {e}") from e

    def retrieve_image_from_url(self, url):
        response = requests.get(url)
        return Image.open(BytesIO(response.content))

    def generate_image(self, prompt):
        """Generate image.

        Args:
            prompt (str): Prompt.

        Returns:
            str: Generated image.
        """
        try:
            response = self.client.images.generate(
                model="dall-e-2",
                prompt=prompt,
                size="512x512",
                quality="standard",
                n=1,
            )
        except Exception as e:
            raise OpenAIError(f"An unexpected error occurred: {e}") from e

        return self.retrieve_image_from_url(response.data[0].url)


