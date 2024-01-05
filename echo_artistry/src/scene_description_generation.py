import re
from enum import Enum

from echo_artistry.src import utils

MAX_RETRIES = 5


class CompositeOption(Enum):
    """This enum class is used to define the composite option for the comic.

    MULTIPLE_IMAGES: The comic will be created with multiple images.
    SINGLE_IMAGE: The comic will be created with a single image.
    """
    SINGLE_IMAGE = "single_image"


class SceneDescriptionGenerator:
    def __init__(self):
        self.client = utils.OpenAIClient()

    def rewrite_text_to_comic_story(self, text):
        msg = [
            {"role": "system", "content": f"Rewrite the given text to a comic.\n"
                                          f"At the beginning name the amount of panels, like: Comic strip with [NAME_NUMBER] panels.\n"
                                          f"Than describe each panel with a few and short sentence."},
            {"role": "user", "content": f"TEXT: {text}"},
        ]
        for _ in range(MAX_RETRIES):
            comic_story = self.client.generate_answer(msg)
            if len(comic_story) < \
                    utils.IMAGE_CHARACTER_LENGTH_MAPPING[self.client.image_model_name]["character_length"]:
                return comic_story
            else:
                msg.append({"role": "assistant", "content": comic_story})
                msg.append({"role": "user", "content": f"Keep the content shorter shorter."})

    def generate_description(self, text, composite_option: CompositeOption=CompositeOption.SINGLE_IMAGE):
        """Generate a description of a comic from a text.

        Args:
            text (str): The text to generate the comic description from.
            composite_option (CompositeOption): The composite option for the comic.

        Returns:
            str: The generated description.
        """
        if composite_option == CompositeOption.SINGLE_IMAGE:
            return self.rewrite_text_to_comic_story(text)
        else:
            raise NotImplementedError(f"Composite option {composite_option} not implemented.")
