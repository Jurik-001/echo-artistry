import re

from echo_artistry.src import utils

MAX_RETRIES = 5
MAX_FILE_NAME_LENGTH = 15


class FileNameGenerator:
    def __init__(self, model_name="gpt-3.5-turbo-1106", max_retries=MAX_RETRIES):
        self.client = utils.OpenAIClient(model_name=model_name)
        self.max_retries = max_retries

    def validate_file_name(self, filename):
        if re.match(r"^[a-z0-9_\-]+$", filename) and len(filename) < MAX_FILE_NAME_LENGTH:
            return True
        else:
            return False

    def generate_file_name(self, text):
        msg = [
            {
                "role": "system",
                "content": f"The following text is in a txt file create a file name, that will match following regex: ^[a-z0-9_\-]+$ and is max {MAX_FILE_NAME_LENGTH} char long. \n provide only the name.",
            },
            {"role": "user", "content": f"TEXT: {text}"},
        ]
        for _ in range(self.max_retries):
            file_name = self.client.generate_answer(msg)
            if self.validate_file_name(file_name):
                return file_name
            else:
                msg.append({"role": "assistant", "content": file_name})
                msg.append(
                    {
                        "role": "user",
                        "content": f"The filename does not meet the requirements.",
                    }
                )

        raise Exception("Max retries exceeded.")
