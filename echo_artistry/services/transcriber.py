"""transcriber contains Transcriber class."""

import os
from pathlib import Path

import whisper

from echo_artistry import utils


class Transcriber:
    """Extracts audio from a video file and transcribes it to text."""

    def __init__(self, output_path="audios", store_transcription=True):
        self.transcribe_model = whisper.load_model("base")
        self.store_transcription = store_transcription
        self.output_path = output_path
        if self.store_transcription:
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)

    def _storing_transcription(self, transcript_result, audio_file_path):
        audio_file_name = Path(audio_file_path).stem
        transcription_file_path = Path(
            self.output_path,
            f"transcription_{audio_file_name}.txt",
        )
        utils.write_text_to_file(transcript_result, str(transcription_file_path))

    def transcribe_audio(self, audio_file_path):
        """Transcribes audio to text.

        Args:
            audio_file_path (str): The path to the audio file.

        Returns:
            str: The transcription of the audio file.
        """
        transcript_result = self.transcribe_model.transcribe(audio_file_path)["text"]

        if self.store_transcription:
            self._storing_transcription(transcript_result, audio_file_path)
        return transcript_result
