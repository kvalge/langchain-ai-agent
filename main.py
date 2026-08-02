# to run: python main.py

import time
import sys
from gemini_provider import gemini_response


# Loading animation for better user experience
def loading(message="Processing"):
    for _ in range(3):
        for dot in [".", "..", "..."]:
            sys.stdout.write(f"\r{message}{dot}")
            sys.stdout.flush()
            time.sleep(0.3)
    print("\r", end="")


# Application header
def banner():
    print("Gemini LLM CLI Application")


def main():
    banner()
    print("Enter your prompt below. Type 'exit()' to quit.\n")

    while True:
        # Read user input
        prompt = input("Prompt: ").strip()

        # Exit condition
        if prompt.lower() in ["exit", "exit()", "quit"]:
            print("\nExiting the application.\n")
            break

        if not prompt:
            print("Please enter a valid prompt.\n")
            continue

        loading("Generating response")

        try:
            output = gemini_response(prompt)
            print(f"\nResponse:\n{output}\n")

        except Exception as e:
            print(f"\nAn error occurred: {e}\n")


if __name__ == "__main__":
    main()