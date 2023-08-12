import os

import openai

from src.config import cfg
from src.logger import logger


class Openai:
    def __init__(self, key="", prompt="", model="gpt-4"):
        self.set_openai_key(key)
        self.system_prompt = self.get_system_prompt(
            f"{cfg.OPENAI_PROMPTS_PATH}/{prompt}"
        )
        self.model = model
        logger.info(f"OpenAI model initialized. Model: {model}. Prompt: {prompt}")

    @staticmethod
    def get_system_prompt(filename):
        with open(filename, encoding="UTF-8") as f:
            return "".join(f.readlines())

    @staticmethod
    def set_openai_key(key):
        openai.api_key = key

        # if null then set to env key
        if not openai.api_key:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            return "Successful"

        if not openai.api_key:
            print(
                "No API key detected. Please set the API key in the addon preferences."
            )
            return

    def generate_message(self, content):
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": content},
        ]  # Set the system prompt

    @staticmethod
    def get_text_from_response(response):
        completion_text = ""

        for event in response:
            if "role" in event["choices"][0]["delta"]:
                # skip
                continue
            if len(event["choices"][0]["delta"]) == 0:
                # skip
                continue
            event_text = event["choices"][0]["delta"]["content"]
            completion_text += event_text  # append the text

        return completion_text

    def generate_response(self, content):
        logger.info("Getting response...")
        messages = self.generate_message(content)  # Generate message for chat
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            stream=True,
            max_tokens=1500,
        )
        return self.get_text_from_response(response)


def run_openai_generation(input_data: str, prompt: str):
    model = Openai(cfg.OPENAI_API_KEY, prompt)
    return model.generate_response(input_data)
