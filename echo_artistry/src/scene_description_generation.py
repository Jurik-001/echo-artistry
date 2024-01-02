import re

from echo_artistry.src import utils

MAX_RETRIES = 5

class SceneDescriptionGenerator:
    def __init__(self):
        self.client = utils.OpenAIClient()

    def extract_number(self, text):
        """
        This function takes a text and extracts the first number in it.
        """
        number = re.findall(r"\d+", text)[0]
        return int(number)

    def retrieve_scene_number(self, text):
        conversation = []
        conversation.append({"role": "system",
             "content": f"The given text should be transformed into a movie, "
                        f"how many scenes can be created based on that. "
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
            {"role": "system", "content": f"You are an artist."
                                          f"Describe based on the text from the user: {scene_number} visual scenes time ordered."
                                          f"Each scene description should cover:\n"
                                          f"- Set the Scene: Describe the location, time of day, and any relevant environmental details.\n"
                                          f"- Introduce Characters: Include characters present in the scene and their physical and emotional states.\n"
                                          f"- Describe the Action: Clearly articulate what is happening in the scene.\n"
                                          f"- Invoke the Senses: Encourage the use of sensory details to create a vivid image.\n"
                                          f"- Emotional Tone: Reflect the scene's emotional impact or mood.\n"},
            {"role": "user", "content": f"{text}"},
        ]
        return self.client.generate_answer(mg)

    def cut_into_scenes(self, text):
        """
        This function takes a text with multiple scenes and splits it into separate scenes.
        Each scene is separated by the keyword "Scene X:\n" where X is a number.
        """
        scenes = text.split("Scene ")

        scenes = [scene for scene in scenes if scene.strip()]

        scenes = ["Scene " + scene for scene in scenes]

        return scenes

    def insert_text_after_scene_title(self, text, scene_number, insertion):
        scenes = text.split("Scene ")

        scenes = [scene for scene in scenes if scene.strip()]

        for i in range(len(scenes)):
            if scenes[i].startswith(str(scene_number) + ":"):
                scene_title, scene_content = scenes[i].split("\n", 1)
                scenes[i] = insertion + "\n" + scene_content
                break

        modified_text = "Scene ".join(scenes)

        return modified_text

    def refine_image_description(self, text):
        refined_image_prompt = [
            {"role": "system", "content": f"You are an artist."
                                          "Rewrite and enrich the scene description using only keywords and short phrases. The result should be so descreptive that an artist can paint an image based on."},
            {"role": "user", "content": f"DESCRIPTION: {text}"},
        ]
        return self.client.generate_answer(refined_image_prompt)

    def generate_description(self, text):
        scene_number = self.retrieve_scene_number(text)

        scene_description = self.retrieve_scene_description(text, scene_number)

        scenes = self.cut_into_scenes(scene_description)

        for i in range(len(scenes)):
            scenes[i] = self.refine_image_description(scenes[i])

        return scenes