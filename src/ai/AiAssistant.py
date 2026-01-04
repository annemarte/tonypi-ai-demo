from openai import OpenAI

class AiAssistant:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def ask(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content