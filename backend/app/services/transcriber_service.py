import assemblyai as aai
from app.config import settings

# Initialize AssemblyAI API key
aai.settings.api_key = settings.ASSEMBLYAI_API_KEY


class TranscriberService:
    def __init__(self):
        self.config = aai.TranscriptionConfig(
            speech_model=aai.SpeechModel.best,
            language_detection=True
        )
        self.transcriber = aai.Transcriber()

    def transcribe_audio(self, audio_file_path: str) -> aai.Transcript:
        """Transcribes audio and returns the AssemblyAI transcript object."""
        transcript = self.transcriber.transcribe(audio_file_path, config=self.config)

        if transcript.status == aai.TranscriptStatus.error:
            raise RuntimeError(f"Transcription failed: {transcript.error}")

        return transcript