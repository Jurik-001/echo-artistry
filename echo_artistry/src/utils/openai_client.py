"""OpenAI API client."""
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
from echo_artistry.src import utils
from echo_artistry.src import exceptions


class OpenAIClient:
    """OpenAI API client."""
    cost_manager = None

    def __init__(
        self,
        model_name=utils.DEFAULT_MODEL_NAME,
        image_model_name=utils.DEFAULT_IMAGE_MODEL_NAME,
        image_size=utils.DEFAULT_IMAGE_SIZE,
        image_quality=utils.DEFAULT_IMAGE_QUALITY,
    ):
        self.model_name = model_name
        self.image_model_name = image_model_name
        self.image_size = image_size
        self.image_quality = image_quality
        self.client = OpenAI()
        if OpenAIClient.cost_manager is None:
            OpenAIClient.cost_manager = utils.CostManager(self.model_name, self.image_model_name, self.image_quality)

    def calculate_cost(self, messages, is_input=True, is_image=False):
        if is_image:
            self.cost_manager.calculate_cost_image(messages)
        else:
            self.cost_manager.calculate_cost_messages(messages, is_input=is_input)

    def generate_answer(self, messages):
        """Generate answer.

        Args:
            messages (list(str)): List of messages.

        Returns:
            str: Generated answer.
        """
        self.calculate_cost(messages, is_input=True, is_image=False)
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
            )
            utils.logger.debug(
                f"Messages: {messages} Response: {response.choices[0].message.content}"
            )
            result = response.choices[0].message.content
            self.calculate_cost(messages, is_input=False, is_image=False)
            return result
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
        self.calculate_cost(prompt, is_input=True, is_image=True)
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
                    "The given text contains content which violates the OpenAI content policy."
                )
            else:
                raise exceptions.OpenAIError(f"An unexpected error occurred: {e}") from e

        return self.retrieve_image_from_url(response.data[0].url)
