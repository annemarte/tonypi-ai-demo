import time
import sys
from pathlib import Path

# Add src folder to path for stubs
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Also add TonyPi HiwonderSDK paths
tonypi_paths = [
    '/home/pi/TonyPi/tonypi2025/HiwonderSDK',
    '/home/pi/TonyPi/HiwonderSDK',
]
for p in tonypi_paths:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    # Real hardware (on TonyPi)
    import hiwonder.ActionGroupControl as AGC
    from hiwonder.Controller import Controller
    import hiwonder.ros_robot_controller_sdk as rrc
    import hiwonder.yaml_handle as yaml_handle
    SIMULATION_MODE = False
except ImportError:
    # Stubs for local development
    import stubs.ActionGroupControl as AGC
    from stubs.Controller import Controller
    import stubs.ros_robot_controller_sdk as rrc
    import stubs.yaml_handle as yaml_handle
    SIMULATION_MODE = True
    print("[WARNING] Running in simulation mode - no real hardware")
class TonyPiController:

    last_cmd_time = 0
    CMD_COOLDOWN = 1.5  # seconds

    def __init__(self, serial_port):
        self.serial_port = serial_port
        board = rrc.Board()
        ctl = Controller(board)

        servo_data = yaml_handle.get_yaml_data(yaml_handle.servo_file_path)
        ctl.set_pwm_servo_pulse(1, 1500, 500)
        ctl.set_pwm_servo_pulse(2, servo_data['servo2'], 500)
        AGC.runActionGroup('stand')
        pass

    def move(self, action: str):
        now = time.time()
        if self.last_cmd_time != 0 and now - self.last_cmd_time < self.CMD_COOLDOWN:
            return
        self.last_cmd_time = now
        print(f"[Robot] Executing action: {action}")
        
        AGC.runActionGroup(action, 2, True)
        