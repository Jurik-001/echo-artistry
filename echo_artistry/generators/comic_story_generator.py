"""comic_story_generator contains ComicStoryGenerator and CompositeOption class."""
import os
from enum import Enum

from echo_artistry import utils

MAX_RETRIES = 5
MAX_FILE_NAME_LENGTH = 15


class CompositeOption(Enum):
    """CompositeOption defines the composite option for the comic."""

    SINGLE_IMAGE = "single_image"


class ComicStoryGenerator:
    """ComicStoryGenerator generates comic stories."""

    def __init__(
        self,
        client,
        output_path="comic_stories",
        max_retries=MAX_RETRIES,
        store_comic_story=True,
    ):
        self.client = client
        self.max_retries = max_retries
        self.output_path = output_path
        self.store_comic_stories = store_comic_story
        if self.store_comic_stories:
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)

    def rewrite_text_to_comic_story(self, text):
        """Rewrite a text to a comic story.

        Args:
            text (str): The text to rewrite to a comic story.

        Returns:
            str: The comic story.
        """
        msg = [
            {
                "role": "system",
                "content": f"Rewrite the given text to a comic.\n"
                f"At the beginning name the amount of panels, like: "
                           f"Comic strip with [NAME_NUMBER] panels.\n"
                f"Than describe each panel with a few and short sentence.",
            },
            {"role": "user", "content": f"TEXT: {text}"},
        ]
        for _ in range(MAX_RETRIES):
            comic_story = self.client.generate_answer(msg)
            if (
                len(comic_story)
                < utils.IMAGE_CHARACTER_LENGTH_MAPPING[self.client.image_model_name][
                    "character_length"
                ]
            ):
                return comic_story
            else:
                msg.append({"role": "assistant", "content": comic_story})
                msg.append(
                    {"role": "user", "content": f"Keep the content shorter shorter."},
                )

        raise Exception("Max retries exceeded.")

    def generate_story(
        self,
        text,
        composite_option: CompositeOption = CompositeOption.SINGLE_IMAGE,
        file_name="comic.txt",
    ):
        """Generate a comic description from a text.

        Args:
            text (str): The text to generate the comic description from.
            composite_option (CompositeOption): The composite option for the comic.
            file_name (str): The name of the file to store the comic story.

        Returns:
            str: The generated description.
        """
        if composite_option == CompositeOption.SINGLE_IMAGE:
            comic_story = self.rewrite_text_to_comic_story(text)
        else:
            raise NotImplementedError(
                f"Composite option {composite_option} not implemented.",
            )

        if self.store_comic_stories:
            comic_story_path = f"{self.output_path}/{file_name}"
            utils.write_text_to_file(comic_story, comic_story_path)

        return comic_story
