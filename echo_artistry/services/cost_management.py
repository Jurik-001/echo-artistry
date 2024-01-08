"""cost_management contains CostManager."""

from echo_artistry.utils import helper


class CostManager:
    """CostManager is used to calculate the cost of a text."""

    total_cost = 0

    def __init__(
        self,
        token_counter,
        model_name=helper.DEFAULT_MODEL_NAME,
        image_model_name=helper.DEFAULT_IMAGE_MODEL_NAME,
        image_quality=helper.DEFAULT_IMAGE_QUALITY,
        image_size=helper.DEFAULT_IMAGE_SIZE,
    ):
        self.token_counter = token_counter
        self.model_name = model_name
        self.image_model_name = image_model_name
        self.image_quality = image_quality
        self.image_size = image_size
        self.input_token_cost = helper.MODEL_TOKEN_LENGTH_MAPPING[model_name][
            "input_token_cost"
        ]
        self.output_token_cost = helper.MODEL_TOKEN_LENGTH_MAPPING[model_name][
            "output_token_cost"
        ]
        self.per_n_tokens = 1000

    def calculate_cost_token(self, token_count, is_input=True):
        """Calculate the cost of a text.

        Args:
            token_count (int): The number of tokens in the text.
            is_input (bool, optional): Whether text is input or output. Defaults to True.

        Returns:
            float: The cost of the text.
        """
        if is_input:
            cost = (token_count / self.per_n_tokens) * self.input_token_cost
        else:
            cost = (token_count / self.per_n_tokens) * self.output_token_cost
        self.total_cost += cost
        return cost

    def calculate_cost_text(self, text, is_input=True):
        """Calculate the cost of a text.

        Args:
            text (str): The text to calculate the cost of.
            is_input (bool, optional): Whether the text is an input or an output.
                Defaults to True.

        Returns:
            float: The cost of the text.
        """
        token_count = self.token_counter.count_tokens(text)
        return self.calculate_cost_token(token_count, is_input=is_input)

    def calculate_cost_messages(self, messages, is_input=True):
        """Calculate the cost of a message.

        Args:
            messages (list): The message to calculate the cost of.
            is_input (bool, optional): Whether the message is an input or an output.
                Defaults to True.

        Returns:
            float: The cost of the message.
        """
        for message in messages:
            text = message["content"]
            self.calculate_cost_text(text, is_input=is_input)

    def calculate_cost_image(self, image):
        """Calculate the cost of an image.

        Args:
            image (Image): The image to calculate the cost of.

        Returns:
            float: The cost of the image.
        """
        image_size = image.size
        image_size_string = f"{image_size[0]}x{image_size[1]}"
        cost = helper.IMAGE_CHARACTER_LENGTH_MAPPING[self.image_model_name][
            "cost_per_image"
        ][self.image_quality][image_size_string]
        self.total_cost += cost
        return cost

    def get_total_cost(self):
        """Get the total cost of the text.

        Returns:
            float: The total cost of the text.
        """
        return self.total_cost
