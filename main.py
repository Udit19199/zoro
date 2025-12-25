import argparse
import os
from google import genai
from dotenv import load_dotenv
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    try:
        for _ in range(0, 20):
            done = generate_content(client, messages, args.verbose)
            if done:
                break
    except Exception as e:
        print(e)


def generate_content(client, messages, verbose):
    # --- Call API ---
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    # --- Validate Response ---
    usage = response.usage_metadata
    if not usage:
        raise RuntimeError("Gemini API response appears to be malformed")

    # --- Add candidates to conversation history ---
    for candidate in response.candidates:
        messages.append(candidate.content)

    has_function_calls = (
        response.function_calls is not None and len(response.function_calls) > 0
    )

    # --- If no tool/function calls, just print normal text ---
    if not has_function_calls:
        print("Response:")
        print(response.text)
        return True

    # Handle function/tool calls
    else:
        function_call_results = []

        for call in response.function_calls:
            result = call_function(call, verbose)

            if not result.parts:
                raise Exception("Function called returned no parts")

            first_part = result.parts[0]

            if (
                not first_part.function_response
                or first_part.function_response.response is None
            ):
                raise RuntimeError("Function returned invalid reponse")

            function_call_results.append(first_part)

            if verbose:
                print(f"-> {first_part.function_response.response}")

            messages.append(types.Content(role="user", parts=function_call_results))

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    return False


if __name__ == "__main__":
    main()
