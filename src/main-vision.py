import json
import time
from pathlib import Path

from ai.decision import DecisionMaker
from ai.vision import VisionAnalyzer
from robot.controller import TonyPiController
from robot.speech import Speaker
from vision.camera import Camera


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "settings.json"
CAPTURE_PATH = PROJECT_ROOT / "captures" / "latest.jpg"


def load_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as config_file:
        config = json.load(config_file)

    required_keys = {
        "openai_api_key",
        "vision_model",
        "camera_index",
        "dry_run",
    }

    missing_keys = required_keys - config.keys()

    if missing_keys:
        raise RuntimeError(
            f"Mangler innstillinger i {CONFIG_PATH}: "
            f"{', '.join(sorted(missing_keys))}"
        )

    return config


def run_once() -> None:
    config = load_config()

    camera = Camera(camera_index=config["camera_index"])

    vision = VisionAnalyzer(
        api_key=config["openai_api_key"],
        model=config["vision_model"],
    )

    decision_maker = DecisionMaker(
        api_key=config["openai_api_key"],
        model=config["vision_model"],
    )

    speaker = Speaker(
        api_key=config["openai_api_key"],
        model=config.get("tts_model", "gpt-4o-mini-tts"),
        voice=config.get("tts_voice", "alloy"),
        dry_run=config["dry_run"],
    )

    robot = TonyPiController(dry_run=config["dry_run"])

    print("\n1. Tar bilde ...")
    image_path = camera.capture(CAPTURE_PATH)
    print(f"   Bilde lagret: {image_path}")

    print("\n2. AI beskriver situasjonen ...")
    situation = vision.describe(image_path)
    print(f"   Situasjon: {situation}")

    print("\n3. Roboten forteller hva den ser ...")
    speaker.say(situation)

    print("\n4. AI velger handling ...")
    decision = decision_maker.choose_action(situation)
    print(f"   Handling: {decision.action}")
    print(f"   Begrunnelse: {decision.reason}")

    print("\n5. TonyPi utfører handling ...")
    robot.execute(decision.action)

    print("\nFerdig.")


def main() -> None:
    try:
        run_once()
    except KeyboardInterrupt:
        print("\nAvbrutt.")
    except Exception as error:
        print(f"\nDemoen feilet: {error}")
        raise


if __name__ == "__main__":
    main()