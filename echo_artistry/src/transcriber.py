"""Extracts audio from a video file and transcribes it to text."""

import os

import whisper

from pathlib import Path


class Transcriber:
    """Extracts audio from a video file and transcribes it to text.

    Attributes:
        output_path (str): The path to the output directory.
    """

    def __init__(self, output_path="audios"):
        self.output_path = output_path
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        self.transcribe_model = whisper.load_model("base")

    def transcribe_audio(self, audio_file_path):
        """Transcribes audio to text.

        Args:
            audio_file_path (str): The path to the audio file.

        Returns:
            str: The path to the transcription file.
        """
        transcript_result = self.transcribe_model.transcribe(audio_file_path)

        audio_file_extension = Path(audio_file_path).suffix

        transcription_file_path = audio_file_path.replace(audio_file_extension, ".txt")

        with open(transcription_file_path, "w") as f:
            f.write(transcript_result["text"])

        return transcription_file_path


