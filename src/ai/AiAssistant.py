from openai import OpenAI

class AiAssistant:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def ask(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Du er en robot-kontroller for TonyPi robot. Svar KUN med én enkel handling som: WALK_FORWARD, TURN_LEFT, TURN_RIGHT, WAVE, STOP, LOOK_AROUND. Ingen forklaringer."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content