import sys
import os
from google import genai
from dotenv import load_dotenv
from google.genai import types


def main():
    load_dotenv()

    args = sys.argv[1:]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    user_prompt = " ".join(args)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    usage = response.usage_metadata
    if usage:
        if "--verbose" in args:
            print("User prompt:", user_prompt)
            print("Prompt tokens:", usage.prompt_token_count)
            print("Response tokens:", usage.candidates_token_count)
        print("Response:")
        print(response.text)


if __name__ == "__main__":
    main()
