import openai
from config import Config
from prompt import Prompt

class LLMClient:
    def __init__(self, config: Config):
        self.config = config
        # pass the key directly; the new OpenAI client ignores
        # openai.api_key, so either give it explicitly or set
        # the OPENAI_API_KEY env var.
        self.prompt_generator = Prompt(config)
        self.client = openai.OpenAI(api_key=self.config.api_key)

    def generate_response(self, user_input: str, additional_messages: list[str]) -> str:
        prompt = self.prompt_generator.create_prompt(user_input, additional_messages)
        response = self.client.chat.completions.create(
            model=self.config.model_name,
            messages=[{"role": "system", "content": prompt}],
            temperature=float(self.config.temperature),
            max_tokens=self.config.token_limit
        )
        return response
    
    def new_generate_response(self, user_input: str, additional_messages: list[str]) -> str:
        prompt = self.prompt_generator.create_new_prompt(additional_messages)
        response = self.client.responses.create(
            model=self.config.model_name,
            instructions=prompt,
            input=user_input,
            max_output_tokens=self.config.token_limit,
        )
        # the new Responses API returns a Response object; for simple text
        # we can call `.output_text` convenience property
        return getattr(response, "output_text", response)
