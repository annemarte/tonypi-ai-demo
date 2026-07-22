#!/usr/bin/python3
# coding=utf8
# Kapsler inn touch-sensor-logikken fra
# TonyPi/Extend/sensor_course/sensor_example/touch_buzzer.py, slik at den kan
# brukes fra andre skript (f.eks. main-touch.py) uten å duplisere GPIO-koden.
import time

import gpiod
from gpiod.line import Direction, Bias, Value

GPIOCHIP = "/dev/gpiochip4"
TOUCH_LINE = 22


class TouchSensor:
    def __init__(
        self,
        chip_path: str = GPIOCHIP,
        line: int = TOUCH_LINE,
        consumer: str = "touch",
    ):
        self.line = line
        self.request = gpiod.request_lines(
            chip_path,
            consumer=consumer,
            config={line: gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_UP)},
        )

    def is_touched(self) -> bool:
        # Sensoren rapporterer INACTIVE (lav) når den blir berørt
        # (se touch_buzzer.py).
        return self.request.get_value(self.line) == Value.INACTIVE

    def wait_for_touch(self, poll_interval: float = 0.05) -> None:
        # Vent først til sensoren ikke lenger er berørt, slik at vi ikke
        # trigger umiddelbart hvis den allerede er i berørt tilstand.
        while self.is_touched():
            time.sleep(poll_interval)

        while not self.is_touched():
            time.sleep(poll_interval)

    def release(self) -> None:
        self.request.release()

    def __enter__(self) -> "TouchSensor":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()
