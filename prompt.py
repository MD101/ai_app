from config import Config
import yaml

class Prompt:
    def __init__(self, config: Config, hidden: int = 0):
        self.sys_prompt = self.load_system_prompt(hidden)
        self.config = config

    def create_prompt(self, user_input: str, additional_messages: list[str]) -> str:
        # Create a prompt based on the user input and configuration
        prompt = f"System: {self.sys_prompt}\n"
        for msg in additional_messages:
            prompt += f"Additional Message: {msg}\n"
        prompt += f"User Input: {user_input}\n"
        return prompt
    
    def create_new_prompt(self, additional_messages: list[str]) -> str:
        # Create a new prompt format based on the user input and configuration
        prompt = f"System: {self.sys_prompt}\n"
        for msg in additional_messages:
            prompt += f" Consider the following instructions only after the user input:Additional Message: {msg}\n"
        return prompt
    
    def load_system_prompt(self, hidden:int) -> str:
        # Load the system prompt from a file or environment variable
        with open("prompt.yaml", "r") as file:
            data = yaml.safe_load(file)
            return data.get(f"system{hidden}", "You are a helpful assistant.")
