import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize Kimi (Moonshot AI) client
client = OpenAI(
    api_key=os.getenv("KIMI_API_KEY", "").strip(),
    base_url="https://api.moonshot.ai/v1"
)

DATA_FILE = "output/quest_data.json"

def _is_valid_mission(item):
    return (
        isinstance(item, dict)
        and item.get('question')
        and item.get('correct')
        and isinstance(item.get('distractors'), list)
        and len(item['distractors']) >= 1
        and item.get('explanation')
    )

def fetch_missions_from_ai():
    """Generates 5 interactive fraction problems with distractors and explanations."""
    
    system_instruction = (
        "You are an expert Grade 5 math educator. Strictly output ONLY JSON. "
        "Constraint: Keep all whole numbers under 500 and denominators under 13. "
        "Focus on Grade 5 fractions (addition, subtraction, multiplication, and division)."
    )
    
    user_prompt = (
        "Generate 5 math word problems for a 5th grader. Theme: Space exploration. "
        "For each problem, provide exactly these four keys:\n"
        "1. 'question': The story problem.\n"
        "2. 'correct': The precise right answer (as a string).\n"
        "3. 'distractors': A list of 3 plausible but incorrect answers.\n"
        "4. 'explanation': A short 2-step solution path for the 'Data Node'.\n"
        "Format: Return a JSON list of objects."
    )
    
    try:
        response = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        
        raw_content = response.choices[0].message.content
        
        # Use regex to find the JSON array in case the AI adds conversational filler
        match = re.search(r'\[.*\]', raw_content, re.DOTALL)
        
        if match:
            data = json.loads(match.group())
            
            # Ensure output directory exists before saving
            os.makedirs("output", exist_ok=True)
            with open(DATA_FILE, "w") as f:
                json.dump(data, f)
            return data
            
    except Exception as e:
        print(f"Error fetching from Kimi: {e}")
        
    return []

def get_current_missions():
    """
    Loads existing missions from local storage. 
    If the file is missing or formatted incorrectly, it fetches new data.
    """
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                # Validation: check if first item has the new 'distractors' key
                if data and isinstance(data, list) and all(_is_valid_mission(m) for m in data):
                    return data
        except (json.JSONDecodeError, KeyError, IndexError):
            pass # Fall through to fetch new data
            
    return fetch_missions_from_ai()
