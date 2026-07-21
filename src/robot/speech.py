import subprocess
import tempfile
from pathlib import Path

from openai import OpenAI


class Speaker:
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini-tts",
        voice: str = "alloy",
        dry_run: bool = True,
    ):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.voice = voice
        self.dry_run = dry_run

    def say(self, text: str) -> None:
        text = text.strip()

        if not text:
            return

        print(f"[ROBOT] sier: {text}")

        if self.dry_run:
            return

        try:
            audio_path = self._synthesize(text)
        except Exception as error:
            print(f"[ROBOT] Kunne ikke generere tale: {error}")
            return

        self._play_audio(audio_path)

    def _synthesize(self, text: str) -> Path:
        audio_path = Path(tempfile.gettempdir()) / "tonypi_speech.mp3"

        with self.client.audio.speech.with_streaming_response.create(
            model=self.model,
            voice=self.voice,
            input=text,
        ) as response:
            response.stream_to_file(audio_path)

        return audio_path

    @staticmethod
    def _play_audio(audio_path: Path) -> None:
        players = (
            ["mpg123", str(audio_path)],
            ["ffplay", "-nodisp", "-autoexit", str(audio_path)],
            ["aplay", str(audio_path)],
        )

        for player in players:
            try:
                subprocess.run(
                    player,
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return
            except (FileNotFoundError, subprocess.CalledProcessError):
                continue

        print(
            f"[ROBOT] Fant ingen avspiller for lydfilen {audio_path}, "
            "lyden ble ikke spilt av."
        )
