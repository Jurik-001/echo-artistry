import re
from enum import Enum

from echo_artistry.src import utils

MAX_RETRIES = 5
IMAGE_STYLE = "Style: Stylized, Digital Illustration, Luminous, Enchanting, Child-friendly, Warm Palette, Whimsical, Expressive Features, Soft Textures\n"


class CompositeOption(Enum):
    """This enum class is used to define the composite option for the comic.

    MULTIPLE_IMAGES: The comic will be created with multiple images.
    SINGLE_IMAGE: The comic will be created with a single image.
    """
    MULTIPLE_IMAGES = "multiple_images"
    SINGLE_IMAGE = "single_image"


class SceneDescriptionGenerator:
    def __init__(self):
        self.client = utils.OpenAIClient()

    def extract_number(self, text):
        """
        This function takes a text and extracts the first number in it.
        """
        number = re.findall(r"\d+", text)[0]
        return int(number)

    def retrieve_panel_number(self, text):
        conversation = []
        conversation.append({"role": "system",
             "content": f"The given text should be transformed into a comic, "
                        f"how many panels can be created based on that. "
                        f"Name ONLY a number between 1 and 10."})
        conversation.append({"role": "user", "content": f"TEXT: {text}"})

        for _ in range(MAX_RETRIES):
            response = self.client.generate_answer(conversation)
            try:
                return self.extract_number(response)
            except IndexError:
                conversation.append({"role": "assistant", "content": response})
                conversation.append({"role": "user", "content": f"Your answer is wrong, please try again."})

    def retrieve_scene_description(self, text, scene_number):
        mg = [
            {"role": "system", "content": f"You are a comic author."
                                          f"Describe based on the text from the user, {scene_number} panels time ordered."
                                          f"Each panel description should cover:\n"
                                          f"- Set the panel: Describe the location, time of day, and any relevant environmental details.\n"
                                          f"- Introduce Characters: Include characters present in the panel and their physical and emotional states.\n"
                                          f"- Describe the Action: Clearly articulate what is happening in the panel.\n"
                                          f"- Invoke the Senses: Encourage the use of sensory details to create a vivid image.\n"
                                          f"- Emotional Tone: Reflect the panels's emotional impact or mood.\n"},
            {"role": "user", "content": f"{text}"},
        ]
        return self.client.generate_answer(mg)

    def cut_into_panels(self, text):
        """
        This function takes a text with multiple scenes and splits it into separate scenes.
        Each scene is separated by the keyword "Scene X:\n" where X is a number.
        """
        scenes = text.split("Panel ")

        scenes = [scene for scene in scenes if scene.strip()]

        scenes = ["Panel " + scene for scene in scenes]

        return scenes

    def refine_image_description(self, text, style_placeholder):
        refined_image_conversation = [
            {"role": "system", "content": f"You are an artist."
                                          "Rewrite and enrich the panel description using only keywords and short phrases. The result should be so descreptive that an artist can paint an image based on."},
            {"role": "user", "content": f"DESCRIPTION: {text}"},
        ]
        for _ in range(MAX_RETRIES):
            refined_image_prompt = self.client.generate_answer(refined_image_conversation)
            if (len(refined_image_prompt) + style_placeholder) < utils.IMAGE_CHARACTER_LENGTH_MAPPING[self.client.image_model_name]["character_length"]:
                return refined_image_prompt
            else:
                refined_image_conversation.append({"role": "assistant", "content": refined_image_prompt})
                refined_image_conversation.append({"role": "user", "content": f"Keep your message shorter."})

    def generate_description(self, text, composite_option: CompositeOption=CompositeOption.MULTIPLE_IMAGES):
        panel_number = self.retrieve_panel_number(text)

        panel_description = self.retrieve_scene_description(text, panel_number)

        if composite_option == CompositeOption.SINGLE_IMAGE:
            panel_description = self.refine_image_description(panel_description, len(IMAGE_STYLE))
            return panel_description
        elif composite_option == CompositeOption.MULTIPLE_IMAGES:
            scenes = self.cut_into_panels(panel_description)

            for i in range(len(scenes)):
                scenes[i] = self.refine_image_description(scenes[i], len(IMAGE_STYLE))
                scenes[i] = IMAGE_STYLE + scenes[i]
            return scenes
        else:
            raise ValueError(f"Invalid composite option: {composite_option}")