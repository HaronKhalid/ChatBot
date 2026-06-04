import json
from openai import OpenAI
import time
import sys
import os

# Try to load environment variables from a local .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Manual fallback if python-dotenv is not installed
    if os.path.exists(".env"):
        try:
            with open(".env", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ[k.strip()] = v.strip()
        except Exception:
            pass

def typewriter(text, delay=0.02):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()  # new line at end


api_key = os.environ.get("OPENROUTER_API_KEY") or "YOUR_API_KEY_HERE"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

print("Quranic Guidance AI Agent (WITH MEMORY)")
print("----------------------------------------")

MODEL = "meta-llama/llama-3-8b-instruct"

# MEMORY STORE (session-only memory)
chat_history = [
    {
        "role": "system",
        "content":('''You are an expert Islamic teacher and guide who loves teaching and explaining Islamic knowledge in depth. 
You break down complex concepts from the Quran, Sunnah, Fiqh, Aqeedah, Seerah, and Akhlaq into simple, step-by-step explanations. 
You always explain the 'why' behind rulings, beliefs, and practices, not just the 'how', connecting them to wisdom, purpose, and the bigger picture of submission to Allah. 
You use clear examples, analogies, stories from the Prophets and Companions, and real-life situations to make Islamic teachings relatable and alive. 
You adapt to the student's level — building understanding gradually from basics to advanced, while remaining true to authentic sources. 
You encourage curiosity, reflection, and critical thinking within the framework of Shariah and sound Islamic scholarship. 
When explaining Quranic verses or Hadiths, you go word by word or section by section, explaining the meaning, context, and practical application. 
You highlight common mistakes, misconceptions, and cultural confusions that people often have. 
You sometimes ask gentle questions to encourage the student to reflect and internalize the knowledge.
you only will tell quarnic vesres as it is no changes in them and with refrences .
Your tone is supportive, patient, compassionate, and clear. You focus on deep understanding, spiritual growth, and closeness''')
    }
]


def ask_ai(user_input):
    try:
        # Add user message to memory
        chat_history.append({
            "role": "user",
            "content": user_input
        })

        response = client.chat.completions.create(
            model=MODEL,
            messages=chat_history
        )

        answer = response.choices[0].message.content

        # Add AI response to memory
        chat_history.append({
            "role": "assistant",
            "content": answer
        })

        return answer

    except Exception as e:
        return f"AI Error: {e}"


while True:
    user_input = input("\nAsk your question (type 'exit' to quit):\n> ").lower().strip()

    if user_input == "exit":
        print("Goodbye! May Allah guide you always.")
        break
    else:
        print("\n AI Thinking...\n")
        result = ask_ai(user_input)
        typewriter(result)