import hiwonder.ActionGroupControl as AGC


class TonyPiController:
    ACTION_GROUPS = {
        "stand": "stand",
        "wave": "wave",
        "wink": "wink",
        "turn_left": "turn_left",
        "turn_right": "turn_right",
        "walk_forward": "go_forward",
        "step_back": "back",
        "stop": "stand",
    }

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run

    def execute(self, action: str) -> None:
        action_group = self.ACTION_GROUPS.get(action)

        if action_group is None:
            raise ValueError(f"Ikke tillatt robothandling: {action}")

        print(
            f"[ROBOT] action={action}, "
            f"action_group={action_group}, dry_run={self.dry_run}"
        )

        if self.dry_run:
            return

        AGC.runActionGroup(action_group)