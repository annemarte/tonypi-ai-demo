import importlib

from robot.touch_sensor import TouchSensor

main_vision = importlib.import_module("main-vision")


def main() -> None:
    print("Klar. Berør touch-sensoren for å starte vision-demoen ...")

    with TouchSensor() as touch_sensor:
        while True:
            touch_sensor.wait_for_touch()
            print("\nTouch registrert!")

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
