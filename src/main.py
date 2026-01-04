import json
from ai.AiAssistant import AiAssistant
from robot.controller import TonyPiController

def load_config():
    with open('config/mysettings.json', 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    config = load_config()
    ai = AiAssistant(config['openai_api_key'])
    robot = TonyPiController(config['serial_port'])

    print("TonyPi AI Demo - skriv en kommando til roboten!")

    while True:
        cmd = input("> ")
        if cmd == "exit":
            break
        action = ai.ask(f"Konverter kommandoen '{cmd}' til en enkel robot-handling.")
        robot.move(action)
