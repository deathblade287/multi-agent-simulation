import requests
import json

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

prompt_ai1 = "So, what's the most absurd conspiracy theory you've ever heard?"


def get_response(prompt):
    data = json.dumps({
        "model": "llama2-uncensored",
        "prompt": prompt,
        "system": "You are a witty, sarcastic, and quick-witted character. Always respond with humor and a touch of cynicism. Make the conversation as entertaining as possible."
    })
    response = requests.post(
        'http://localhost:11434/api/generate', headers=headers, data=data, stream=True)
    complete_response = ""

    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                json_response = json.loads(decoded_line)
                word = json_response.get("response", "")
                print(word, end="", flush=True)
                complete_response += word
    else:
        print(f"Error: {response.status_code}")

    return complete_response.strip()


conversation = []

try:
    while True:
        # AI 1
        print("\n\nAI 1\n--------------------------\n")
        response_ai1 = get_response(prompt_ai1)
        conversation.append(f"AI1: {response_ai1}")

        # Creating a conversation chain
        prompt_ai2 = response_ai1  # Set AI1's response as the next prompt for AI2

        # AI2's turn
        print("\n\nAI 2\n--------------------------\n")
        response_ai2 = get_response(prompt_ai2)
        conversation.append(f"AI2: {response_ai2}")

        prompt_ai1 = response_ai2  # Set AI2's response as the next prompt for AI1

except KeyboardInterrupt:
    print("\nConversation interrupted by user.")
