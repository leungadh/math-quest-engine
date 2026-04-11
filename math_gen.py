import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()
KIMI_API_KEY = os.getenv("KIMI_API_KEY")

# 2. Initialize the Client
client = OpenAI(
    api_key=KIMI_API_KEY,
    base_url="https://api.moonshot.cn/v1",
)

def generate_math_quest():
    print("🚀 Generating quests and solutions via Kimi...")
    
    # We ask for a specific JSON structure to make parsing easy
    prompt = """
    Generate 5 math word problems for a 5th grader. 
    Topic: Fractions (Addition, Subtraction, Multiplication, and Division).
    Theme: Space exploration.
    Format: Return ONLY a JSON list of objects. 
    Each object must have "question" and "answer" keys.
    """

    try:
        response = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates educational math materials in JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        # Parse the JSON response
        content = response.choices[0].message.content
        data = json.loads(content)
        
        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)
        
        # 3. Write the Student Quest File
        with open("output/math_quest.txt", "w") as q_file:
            q_file.write("--- SPACE FRACTION QUEST ---\n\n")
            for i, entry in enumerate(data, 1):
                q_file.write(f"Problem {i}: {entry['question']}\n\n")
        
        # 4. Write the Solution Key File
        with open("output/solution.txt", "w") as s_file:
            s_file.write("--- SOLUTION KEY ---\n\n")
            for i, entry in enumerate(data, 1):
                s_file.write(f"Problem {i} Answer: {entry['answer']}\n\n")
        
        print("✅ Success! 'math_quest.txt' and 'solution.txt' are ready in /output.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if not KIMI_API_KEY:
        print("Error: KIMI_API_KEY not found in .env file.")
    else:
        generate_math_quest()
