import questionary
from llm_client import LLMClient
from config import Config

config = Config()

instructions = "After the question, Provide additional instructions for the AI model (optional):\n\
Start with 'Additional Message:' followed by your instructions.\nYou can add multiple instructions by separating them with a new line.\n\
If you don't have any additional instructions, do nothing.\n"
def main():
    print("Welcome to the AI App!")
    user_input = questionary.text(f"Please enter your input:\n{instructions}",multiline=True).ask()
    print(f"You entered: {user_input}")

    # segmenting input safely
    segmented_input = user_input.split("Additional Message:")
    if len(segmented_input) > 1:
        # there is an additional message section
        extra = segmented_input[1]
        segments = extra.split(", ")
        additional_messages = [seg.strip() for seg in segments if seg.strip()]
        user_input = segmented_input[0].strip()
    else:
        additional_messages = []
        user_input = user_input.strip()

    llm_client = LLMClient(config)
    response = llm_client.new_generate_response(user_input, additional_messages)
    print(f"AI Response: {response}")

    


if __name__ == "__main__":
    main()
    

