"""OpenAI API client."""
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
from echo_artistry.src import utils
from echo_artistry.src import exceptions


class OpenAIClient:
    """OpenAI API client."""

    def __init__(self, model_name=utils.DEFAULT_MODEL_NAME, image_model_name=utils.DEFAULT_IMAGE_MODEL_NAME, image_size=utils.DEFAULT_IMAGE_SIZE):
        self.model_name = model_name
        self.image_model_name = image_model_name
        self.image_size = image_size
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
            utils.logger.debug(f'Messages: {messages} Response: {response.choices[0].message.content}')
            return response.choices[0].message.content
        except Exception as e:
            raise exceptions.OpenAIError(f"An unexpected error occurred: {e}") from e

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
                model=self.image_model_name,
                prompt=prompt,
                size=self.image_size,
                quality="standard",
                n=1,
            )
        except Exception as e:
            if "content_policy_violation" in str(e):
                raise exceptions.ContentPolicyViolation(
                    "The given text contains content which violates the OpenAI content policy.")
            else:
                raise exceptions.OpenAIError(f"An unexpected error occurred: {e}") from e

        return self.retrieve_image_from_url(response.data[0].url)