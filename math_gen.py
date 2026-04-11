import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()
KIMI_API_KEY = os.getenv("KIMI_API_KEY")

# 2. Initialize the Client
# Kimi uses the OpenAI-compatible SDK
client = OpenAI(
    api_key=KIMI_API_KEY,
    base_url="https://api.moonshot.ai/v1",
)

def generate_math_quest():
    print("🚀 Connecting to Kimi LLM to generate quests...")
    
    prompt = """
    Generate 5 math word problems for a 5th grader. 
    Topic: Fractions (Addition, Subtraction, Multiplication, and Division).
    Theme: Simple space exploration stories.
    Format: Return ONLY a JSON list of strings.
    """

    try:
        response = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates educational math materials."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        # Extract the content
        content = response.choices[0].message.content
        problems = json.loads(content)
        
        # 3. Save to the /output directory (mapped to your MacBook via Docker Volume)
        os.makedirs("output", exist_ok=True)
        file_path = "output/math_quest.txt"
        
        with open(file_path, "w") as f:
            for i, prob in enumerate(problems, 1):
                f.write(f"Problem {i}: {prob}\n\n")
        
        print(f"✅ Success! Quests saved to {file_path}")

    except Exception as e:
        print(f"❌ Error generating problems: {e}")

if __name__ == "__main__":
    if not KIMI_API_KEY:
        print("Error: KIMI_API_KEY not found in .env file.")
    else:
        generate_math_quest()
