import importlib
import threading
from pathlib import Path

from robot.speech import Speaker
from robot.temperature_sensor import read_temperature_humidity
from robot.touch_sensor import TouchSensor

main_vision = importlib.import_module("main-vision")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOUCH_SOUND_PATH = PROJECT_ROOT / "audio" / "heisann.wav"


HUMIDITY_CHANGE_THRESHOLD = 2.0
HUMIDITY_ALERT_MESSAGE = "slutt å pust på meg"
HUMIDITY_CHECK_INTERVAL_SECONDS = 2.0


def monitor_humidity(speaker: Speaker, stop_event: threading.Event) -> None:
    """Kjører i egen tråd og overvåker fuktighetsendringer kontinuerlig."""
    previous_humidity = None

    while not stop_event.is_set():
        try:
            _, humidity = read_temperature_humidity()

            if previous_humidity is not None and abs(humidity - previous_humidity) > HUMIDITY_CHANGE_THRESHOLD:
                print(
                    f"\n   Fuktighetsendring på {abs(humidity - previous_humidity):.1f} % oppdaget!"
                )
                speaker.say(HUMIDITY_ALERT_MESSAGE)

            previous_humidity = humidity
        except Exception as error:
            print(f"\nKunne ikke lese fuktighet i overvåkingstråden: {error}")

        stop_event.wait(HUMIDITY_CHECK_INTERVAL_SECONDS)


def main() -> None:
    print("Klar. Berør touch-sensoren for å starte vision-demoen ...")

    config = main_vision.load_config()
    speaker = Speaker(
        api_key=config["openai_api_key"],
        model=config.get("tts_model", "gpt-4o-mini-tts"),
        voice=config.get("tts_voice", "alloy"),
        dry_run=config["dry_run"],
    )

    stop_event = threading.Event()
    humidity_thread = threading.Thread(
        target=monitor_humidity,
        args=(speaker, stop_event),
        daemon=True,
    )
    humidity_thread.start()

    try:
        with TouchSensor() as touch_sensor:
            while True:
                touch_sensor.wait_for_touch()
                print("\nTouch registrert!")

                speaker.play_file(TOUCH_SOUND_PATH)

                try:
                    temperature, humidity = read_temperature_humidity()
                    print(f"   Temperatur: {temperature:.1f} C, Fuktighet: {humidity:.1f} %")
                except Exception as error:
                    print(f"\nKunne ikke lese temperatur/fuktighet: {error}")
                    temperature, humidity = None, None

                try:
                    main_vision.run_once(temperature=temperature, humidity=humidity)
                except KeyboardInterrupt:
                    raise
                except Exception as error:
                    print(f"\nDemoen feilet: {error}")
    finally:
        stop_event.set()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAvbrutt.")
