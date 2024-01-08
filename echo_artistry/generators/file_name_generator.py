"""file_name_generator contains FileNameGenerator."""

MAX_RETRIES = 5
MAX_FILE_NAME_LENGTH = 35


class FileNameGenerator:
    """A class for generating a file name from a text."""

    def __init__(
        self,
        client,
        max_retries=MAX_RETRIES,
        max_file_name_length=MAX_FILE_NAME_LENGTH,
    ):
        self.client = client
        self.max_file_name_length = max_file_name_length
        self.max_retries = max_retries

    @staticmethod
    def _validate_file_name(filename):
        if len(filename) < MAX_FILE_NAME_LENGTH:
            return True
        else:
            return False

    @staticmethod
    def _sanitize_string(topic):
        topic = topic.lower()
        sanitized = topic.replace(" ", "_")
        sanitized = "".join(char for char in sanitized if char.isalnum() or char == "_")

        return sanitized

    def generate_file_name(self, text):
        """Generate a file name from a text.

        Args:
            text (str): The text to generate a file name from.

        Returns:
            str: The generated file name.
        """
        msg = [
            {
                "role": "system",
                "content": f"Name one important topic in following text.",
            },
            {"role": "user", "content": f"TEXT: {text} \n One topic: [TOPIC]"},
        ]
        for _ in range(self.max_retries):
            file_name = self.client.generate_answer(msg)
            file_name = self._sanitize_string(file_name)
            if self._validate_file_name(file_name):
                return file_name
            else:
                msg.append({"role": "assistant", "content": file_name})
                msg.append(
                    {
                        "role": "user",
                        "content": f"The topic is to long please make it shorter,"
                                   f"max character count: {self.max_file_name_length}.",
                    },
                )

        raise Exception("Max retries exceeded.")
