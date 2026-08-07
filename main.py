import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("Environment variable 'OPENROUTER_API_KEY' is not set or found. Please check your .env file")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "user", "content": args.user_prompt}
    ]

    response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    )

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        if response.usage is None:
            raise RuntimeError("API request contained no usage data, the request may have failed.")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
