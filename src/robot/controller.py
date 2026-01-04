class TonyPiController:
    def __init__(self, serial_port):
        self.serial_port = serial_port
        pass

    def move(self, action: str):
        print(f"[Robot] Executing action: {action}")
        #todo implement the action