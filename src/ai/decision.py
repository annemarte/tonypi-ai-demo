from typing import Literal

from openai import OpenAI
from pydantic import BaseModel


RobotAction = Literal[
    "stand",
    "wave",
    "bow",
    "turn_left",
    "turn_right",
    "walk_forward",
    "step_back",
    "dance",
    "stop",
    "twist",
    "chest",
    "left_uppercut",
    "stand_slow"
]

MAX_ACTIONS = 3


class Decision(BaseModel):
    actions: list[RobotAction]
    reason: str
    speech: str


class DecisionMaker:
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def choose_action(
        self,
        situation: str,
        temperature: float | None = None,
        humidity: float | None = None,
    ) -> Decision:
        user_content = (
            "Situasjonsbeskrivelse fra robotens kamera:\n\n"
            f"{situation}"
        )

        if temperature is not None and humidity is not None:
            user_content += (
                "\n\nSensordata målt av roboten idet den ble berørt:\n"
                f"Temperatur: {temperature:.1f} °C\n"
                f"Fuktighet: {humidity:.1f} %"
            )

        response = self.client.responses.parse(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "Du styrer en liten humanoid robot med en lekende, "
                        "nysgjerrig og litt frempå personlighet. "
                        "Tillatte handlinger er: "
                        f"{', '.join(RobotAction.__args__)}. "
                        f"Velg mellom én og {MAX_ACTIONS} tillatte handlinger, i den "
                        "rekkefølgen de skal utføres. Du kan gjenta samme handling "
                        "flere ganger i listen, f.eks. walk_forward, walk_forward, "
                        "walk_forward for å gå tre skritt framover. Dersom det er "
                        "trygt å gå framover, skal du ALLTID inkludere walk_forward "
                        "minst to ganger i rad (aldri bare én gang), slik at roboten "
                        "tar minst to skritt framover samlet. "
                        f"Med mindre situasjonen krever stop, bør du helst velge "
                        f"{MAX_ACTIONS} handlinger (aldri bare én), for eksempel en "
                        "bevegelse kombinert med en eller flere gester/danser, "
                        "for å gjøre roboten mer levende og underholdende. "
                        "Sikkerhet prioriteres foran underholdning. "
                        "Velg aldri walk_forward dersom situasjonen beskriver "
                        "en hindring, ukjent terreng, en person svært nær roboten "
                        "eller utilstrekkelig informasjon. "
                        "Ved usikkerhet skal listen inneholde stop, og bør "
                        "også inkludere shrug (rist på hodet / trekk på "
                        "skuldrene) for å vise at roboten er usikker, f.eks. "
                        "stop, wink. "
                        "'reason' skal være maks én kort setning som forklarer "
                        "HVORFOR du valgte handlingene (teknisk begrunnelse). "
                        "'speech' er det roboten faktisk skal SI høyt til folk "
                        "rundt seg, skrevet med robotens lekne personlighet, "
                        "maks én kort setning. Hvis sensordata for temperatur og "
                        "fuktighet er tilgjengelig i brukermeldingen, MÅ du "
                        "eksplisitt nevne den faktiske temperatur- og/eller "
                        "fuktighetsverdien i 'speech' (ikke bare i 'reason'), "
                        "f.eks. \"Oi, X grader og Y% fuktighet, det er jo helt herlig!\"."
                    ),
                },
                {
                    "role": "user",
                    "content": user_content,
                },
            ],
            text_format=Decision,
        )

        decision = response.output_parsed

        if decision is None:
            raise RuntimeError("AI returnerte ingen gyldig beslutning")

        if not decision.actions:
            raise RuntimeError("AI returnerte en tom handlingsliste")

        decision.actions = decision.actions[:MAX_ACTIONS]

        return decision