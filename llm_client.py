import openai
from config import Config
from prompt import Prompt
import inspect

class LLMClient:
    def __init__(self, config: Config):
        self.config = config
        self.prompt_generator = Prompt(config)
        self.client = openai.OpenAI(api_key=self.config.api_key)

    def _inspect_response(self, response) ->:
        print("Inspecting response object:")
        print(f"Type: {type(response)}")
        print("Attributes:")
        for attr in dir(response):
            if not attr.startswith("_"):
                print(f" - {attr}")
        print("Methods:")
        for method in inspect.getmembers(response, predicate=inspect.ismethod):
            if not method[0].startswith("_"):
                print(f" - {method[0]}")
    
    def _extract_response_text(self, response) -> str:
        text = getattr(response, "output_text", None)
        if text:
            return text
        parts = []
        for msg in getattr(response, "output", []):
            for block in getattr(msg, "content", []):
                t = getattr(block, "text", None)
                if t:
                    parts.append(t)
        return "\n".join(parts)


    def generate_response(self, user_input: str, additional_messages: list[str], return_raw: bool = False) -> str:
        prompt = self.prompt_generator.create_prompt(user_input, additional_messages)
        try:
            response = self.client.chat.completions.create(
                    model=self.config.model_name,
                    messages=[{"role": "system", "content": prompt}],
                    temperature=float(self.config.temperature),
                    max_tokens=self.config.token_limit
                )
        except Exception as e:
            print(f"Error generating response: {e}")
            raise
        
        text = self._extract_response_text(response)
        return (text, response) if return_raw else text
    
    def new_generate_response(self, user_input: str, additional_messages: list[str], return_raw: bool = False, inspect_it: bool = False) -> str:
        prompt = self.prompt_generator.create_new_prompt(additional_messages)
        try:
            response = self.client.responses.create(
                model=self.config.model_name,
                instructions=prompt,
                input=user_input,
                max_output_tokens=self.config.token_limit,
            )
        # the new Responses API returns a Response object; for simple text
        # we can call `.output_text` convenience property
        # return getattr(response, "output_text", response)
        except Exception as e:
            print(f"Error generating response: {e}")
            raise

        if inspect_it:
            self._inspect_response(response)
        text = self._extract_response_text(response)
        return (text, response) if return_raw else text
