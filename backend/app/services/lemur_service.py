import assemblyai as aai


class LemurService:
    @staticmethod
    def translate_transcript(transcript: aai.Transcript, target_language: str) -> str:
        """Uses AssemblyAI LeMUR to accurately translate transcribed speech."""
        if not transcript.text or not transcript.text.strip():
            return ""

        prompt = (
            f"You are a real-time conversational translator for tourists and locals. "
            f"Translate the following speech transcript accurately and naturally into {target_language}. "
            f"Return ONLY the translated sentence with no commentary, quotation marks, or notes."
        )

        response = transcript.lemur.task(
            prompt=prompt,
            final_model=aai.LemurModel.default
        )

        return response.response.strip()