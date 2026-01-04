import json
import argparse
from ai.AiAssistant import AiAssistant
from robot.controller import TonyPiController

def load_config(settings_file):
    print(f"Loading settings from {settings_file}")
    with open(settings_file, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TonyPi AI Demo")
    parser.add_argument("--settings", default="config/mysettings.json", help="Path to settings file")
    args = parser.parse_args()
    
    config = load_config(args.settings)
    ai = AiAssistant(config['openai_api_key'])
    robot = TonyPiController(config['serial_port'])

    print("TonyPi AI Demo - skriv en kommando til roboten!")

    while True:
        cmd = input("> ")
        if cmd == "exit":
            break
        action = ai.ask(f"Konverter kommandoen '{cmd}' til en enkel robot-handling.")
        robot.move(action)
