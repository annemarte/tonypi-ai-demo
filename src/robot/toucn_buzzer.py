#!/usr/bin/python3
# coding=utf8
# 4.拓展课程学习\7.拓展课程之传感器基础开发课程\第2课 触摸传感器实验(4.Advanced Lessons\7.Sensor Development Course\Lesson2 Touch Sensor Module)
import os
import sys
import time
import gpiod
from gpiod.line import Direction, Bias, Value
import hiwonder.ros_robot_controller_sdk as rrc


board = rrc.Board()

st = 0

request = gpiod.request_lines(
    '/dev/gpiochip4',
    consumer="touch",
    config={22: gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_UP)},
)

if __name__ == '__main__':
    try:
        while True:
            state = request.get_value(22)   #读取引脚数字值(read pin numerical value)
            if state == Value.INACTIVE:
                if st :            #这里做一个判断，防止反复响(make a judgement to prevent repeated ringing here)
                    st = 0
                    board.set_buzzer(1900, 0.1, 0.9, 1) # 以1900Hz的频率，持续响0.1秒，关闭0.9秒，重复1次(at a frequency of 1900Hz, sound for 0.1 seconds, then pause for 0.9 seconds, repeat once)
            else:
                st = 1
                board.set_buzzer(1000, 0.0, 0.0, 1) # 关闭(close)
    finally:
        board.set_buzzer(1000, 0.0, 0.0, 1) # 关闭(close)
        request.release()

