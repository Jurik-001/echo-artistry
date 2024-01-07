"""openai_client contains OpenAIClient class."""
from io import BytesIO

import requests
from openai import OpenAI
from PIL import Image

from echo_artistry import exceptions
from echo_artistry.utils import helper


class OpenAIClient:
    """OpenAI API client."""

    def __init__(
        self,
        cost_manager,
        model_name=helper.DEFAULT_MODEL_NAME,
        image_model_name=helper.DEFAULT_IMAGE_MODEL_NAME,
        image_size=helper.DEFAULT_IMAGE_SIZE,
        image_quality=helper.DEFAULT_IMAGE_QUALITY,
    ):
        self.cost_manager = cost_manager
        self.model_name = model_name
        self.image_model_name = image_model_name
        self.image_size = image_size
        self.image_quality = image_quality
        self.client = OpenAI()

    def _calculate_cost(self, messages=None, image=None, is_input=True):
        if image:
            self.cost_manager.calculate_cost_image(image)
        if messages:
            self.cost_manager.calculate_cost_messages(messages, is_input=is_input)

    def generate_answer(self, messages):
        """Generate answer.

        Args:
            messages (list(str)): List of messages.

        Returns:
            str: Generated answer.
        """
        self._calculate_cost(messages=messages, is_input=True)
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
            )
            helper.logger.debug(
                f"Messages: {messages} Response: {response.choices[0].message.content}",
            )
            result_text = response.choices[0].message.content
        except Exception as e:
            raise exceptions.OpenAIError(f"An unexpected error occurred: {e}") from e

        result_message = [{"role": "assistant", "content": result_text}]
        self._calculate_cost(messages=result_message, is_input=False)
        return result_text

    def _retrieve_image_from_url(self, url):
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
                    "The given text contains content which "
                    "violates the OpenAI content policy.",
                )
            else:
                raise exceptions.OpenAIError(f"An unexpected error occurred: {e}") from e
        image = self._retrieve_image_from_url(response.data[0].url)
        self._calculate_cost(image=image, is_input=True)
        return image
