import os

from echo_artistry.src import utils

MAX_RETRIES = 5


class ComicImageGenerator:
    def __init__(
        self,
        model_name=utils.DEFAULT_IMAGE_MODEL_NAME,
        output_path="comic_images",
        store_comic_images=True,
    ):
        self.client = utils.OpenAIClient(image_model_name=model_name)
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

        Returns:
            str: The generated description.
        """
        comic_image = self.client.generate_image(text)

        if self.store_comic_images:
            comic_image_path = os.path.join(self.output_path, file_name)
            utils.write_text_to_file(comic_image, comic_image_path)

        return comic_image
