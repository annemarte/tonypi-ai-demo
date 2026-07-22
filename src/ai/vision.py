import base64
from pathlib import Path

from openai import OpenAI


class VisionAnalyzer:
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    @staticmethod
    def _encode_image(image_path: Path) -> str:
        image_bytes = image_path.read_bytes()
        return base64.b64encode(image_bytes).decode("utf-8")

    def describe(
        self,
        image_path: str | Path,
        temperature: float | None = None,
        humidity: float | None = None,
    ) -> str:
        image_path = Path(image_path)
        encoded_image = self._encode_image(image_path)

        prompt_text = (
            "Du er en liten humanoid robot med en lekende, "
            "nysgjerrig og litt frempå personlighet. "
            "Beskriv i maks 1 kort setning hva du ser, "
            "med en søt personlighet i formuleringen. "
            "Nevn kort hva du ser og "
            "om det virker trygt å bevege seg fremover. "
            "Ikke velg en robothandling ennå. Vær veldig kort og konsis. Gjerne litt hipp og kul Bærum-slang."
        )

        if temperature is not None and humidity is not None:
            prompt_text += (
                f" Du målte akkurat temperaturen ({temperature:.1f} °C) og "
                f"fuktigheten ({humidity:.1f} %) idet du ble berørt, og du MÅ "
                "nevne disse faktiske verdiene i beskrivelsen, f.eks. "
                f"\"Oi, {temperature:.1f} grader og {humidity:.1f}% fuktighet!\"."
            )

        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": prompt_text,
                        },
                        {
                            "type": "input_image",
                            "image_url": (
                                f"data:image/jpeg;base64,{encoded_image}"
                            ),
                            "detail": "low",
                        },
                    ],
                }
            ],
        )

        description = response.output_text.strip()

        if not description:
            raise RuntimeError("AI returnerte ingen situasjonsbeskrivelse")

        return description