import random
import sys
import time

_HIWONDER_SDK_PATHS = [
    "/home/pi/TonyPi/HiwonderSDK",
    "/home/pi/TonyPi",
]

for _sdk_path in _HIWONDER_SDK_PATHS:
    if _sdk_path not in sys.path:
        sys.path.append(_sdk_path)


class TonyPiController:
    # Alle verdier under er verifisert mot faktiske .d6a-filer i
    # TonyPi/ActionGroups på selve roboten.
    ACTION_GROUPS = {
        "stand": "stand",
        "wave": "wave",
        "wink": "bow",
        "turn_left": "turn_left",
        "turn_right": "turn_right",
        "walk_forward": "go_forward",
        "step_back": "back",
        "stop": "stand",
        "shrug": "twist",
        "16": "16",
        "left_uppercut": "left_uppercut",
    }

    # Ingen egne "dance"-action groups finnes på roboten, så vi bruker
    # eksisterende, dansevennlige bevegelser som varianter.
    DANCE_ACTION_GROUPS = [
        "twist",
        "stepping",
        "wing_chun",
    ]

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run

    def execute_all(self, actions: list, pause_seconds: float = 1.0) -> None:
        for action in actions:
            self.execute(action)

            if not self.dry_run:
                time.sleep(pause_seconds)

    def execute(self, action: str) -> None:
        if action == "dance":
            action_group = random.choice(self.DANCE_ACTION_GROUPS)
        else:
            action_group = self.ACTION_GROUPS.get(action)

        if action_group is None:
            raise ValueError(f"Ikke tillatt robothandling: {action}")

        print(
            f"[ROBOT] action={action}, "
            f"action_group={action_group}, dry_run={self.dry_run}"
        )

        if self.dry_run:
            return

        try:
            import hiwonder.ActionGroupControl as AGC
        except ModuleNotFoundError as error:
            raise ModuleNotFoundError(
                "Fant ikke 'hiwonder'-modulen. Denne modulen finnes kun på "
                "selve TonyPi-roboten (Raspberry Pi) og må kjøres derfra, "
                "eller kjør med dry_run=True for lokal testing."
            ) from error

        AGC.runActionGroup(action_group)