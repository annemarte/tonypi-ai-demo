#!/usr/bin/env python3
# encoding: utf-8
# @Author: Aiden
# @Date: 2024/09/21
import time

from robot.temperature_sensor import read_temperature_humidity


if __name__ == '__main__':
    while True:
        temperature, humidity = read_temperature_humidity()

        print("Temperature: {:.1f} C, Humidity: {:.1f} %".format(temperature, humidity))

        time.sleep(2)
