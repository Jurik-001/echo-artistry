"""comic_image_generator contains the ComicImageGenerator class."""

import os

MAX_RETRIES = 5


class ComicImageGenerator:
    """A class for generating a comic image from a text."""

    def __init__(
        self,
        client,
        output_path="comic_images",
        store_comic_images=True,
    ):
        self.client = client
        self.output_path = output_path
        self.store_comic_images = store_comic_images
        if self.store_comic_images:
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)

    def generate_image(self, text, file_name="comic.png"):
        """Generate a comic description from a text.

        Args:
            text (str): The text to generate the
            composite_option (CompositeOption): The composite option for the comic.
            file_name (str): The name of the file to store the comic description.

        Returns:
            str: The generated description.
        """
        comic_image = self.client.generate_image(text)

        if self.store_comic_images:
            comic_image_path = os.path.join(self.output_path, file_name)
            comic_image.save(comic_image_path)

        return comic_image
