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

    def describe(self, image_path: str | Path) -> str:
        image_path = Path(image_path)
        encoded_image = self._encode_image(image_path)

        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "Beskriv kort hva roboten ser. "
                                "Nevn personer, hindringer, objekter og "
                                "om området foran roboten virker trygt å bevege seg i. "
                                "Ikke velg en robothandling ennå."
                            ),
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