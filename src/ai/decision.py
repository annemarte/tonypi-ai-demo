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


class DecisionMaker:
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def choose_action(self, situation: str) -> Decision:
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
                        "walk_forward for å gå tre skritt framover. "
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
                        "stop, shrug. "
                        "'reason' skal være maks én kort setning, skrevet med "
                        "robotens personlighet."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Situasjonsbeskrivelse fra robotens kamera:\n\n"
                        f"{situation}"
                    ),
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