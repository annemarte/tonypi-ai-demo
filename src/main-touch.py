import importlib
from pathlib import Path

from robot.speech import Speaker
from robot.touch_sensor import TouchSensor

main_vision = importlib.import_module("main-vision")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOUCH_SOUND_PATH = PROJECT_ROOT / "audio" / "heisann.wav"


def main() -> None:
    print("Klar. Berør touch-sensoren for å starte vision-demoen ...")

    config = main_vision.load_config()
    speaker = Speaker(
        api_key=config["openai_api_key"],
        model=config.get("tts_model", "gpt-4o-mini-tts"),
        voice=config.get("tts_voice", "alloy"),
        dry_run=config["dry_run"],
    )

    with TouchSensor() as touch_sensor:
        while True:
            touch_sensor.wait_for_touch()
            print("\nTouch registrert!")

            speaker.play_file(TOUCH_SOUND_PATH)

            try:
                main_vision.run_once()
            except KeyboardInterrupt:
                raise
            except Exception as error:
                print(f"\nDemoen feilet: {error}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAvbrutt.")
