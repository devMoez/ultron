import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv("swarm/.env")

def test_deepseek():
    key = os.environ.get("DEEPSEEK_API_KEY")
    print(f"Key: {key[:8]}...")
    try:
        resp = completion(
            model="deepseek/deepseek-chat",
            messages=[{"role": "user", "content": "Say OK"}],
            api_key=key
        )
        print("Response:", resp.choices[0].message.content)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_deepseek()
