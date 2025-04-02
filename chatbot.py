import ollama
import json
import datetime
from google import genai

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access variables
api_key = os.getenv("API_KEY")

class AIProcessor:
    def __init__(self, api_key):
        self.genai_client = genai.Client(api_key=api_key)

    # Function to get current time
    @staticmethod
    def get_time():
        return datetime.datetime.now().strftime("⏰ The current time is %H:%M:%S")

    # Function to perform calculations
    @staticmethod
    def calculator(expression):
        try:
            result = eval(expression)  # Be cautious! Use safer eval alternatives in real apps.
            return f"🧮 The result of {expression} is {result}"
        except Exception as e:
            return f"⚠️ Error: {str(e)}"

    # Function to process the model's response
    def process_response(self, response):
        try:
            # Ensure response is a dictionary, not a string
            if isinstance(response, str):
                response_json = json.loads(response)
            else:
                response_json = response  # Already a dictionary\

            tool = response_json.get("tool")
            data = response_json.get("data", {})

            if tool == "get_time":
                return self.get_time()
            elif tool == "calculator":
                return self.calculator(data.get("expression", ""))
            else:
                return "⚠️ Unknown tool request."
        except json.JSONDecodeError:
            print("errr")
            return response  # Regular AI response

    # Function to use Gemini for AI responses
    def ask_gemini(self, prompt):
        response = self.genai_client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        return response.text

    # Function to use Ollama for AI responses
    def ask_ollama(self, model, messages):
        response = ollama.chat(model=model, messages=messages)
        return response["message"]["content"]


if __name__ == "__main__":
    with open("input", "r", encoding="utf-8") as file:
        input_string = file.read()

    ai_processor = AIProcessor(api_key)

    while True:
        user_input = input("You: ")
        user_input = input_string + "\n" + user_input
        print(user_input)

        # Ask Ollama for a response (Uncomment if needed)
        # ollama_response = ai_processor.ask_ollama("mcpmodel", [{"role": "user", "content": user_input}])
        # tool_output = ai_processor.process_response(ollama_response)

        # Get Gemini response
        gemini_response = ai_processor.ask_gemini(user_input)
        print(gemini_response)

        # Correctly process the Gemini response
        processed_response = ai_processor.process_response(gemini_response.replace("```json", "").replace("```", "").strip())
        print(processed_response)
