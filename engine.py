import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY", "").strip()
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
        "You are an expert Grade 5 math educator. "
        "Strictly output ONLY a valid JSON array — no preamble, no trailing text. "
        "Every problem MUST be a fractions problem: the operation must involve fractions, "
        "and the answer must be expressed as a fraction or mixed number (e.g. '3/4', '1 1/2'). "
        "Before finalising each problem, mentally verify your answer is arithmetically correct. "
        "Use only denominators 2, 3, 4, 5, 6, 8, or 10. "
        "All intermediate and final values must be expressible as fractions with those denominators."
    )

    user_prompt = (
        "Generate 5 fraction word problems for a 5th grader. "
        "Use everyday daily life themes such as cooking, shopping, sports, gardening, or sharing food.\n\n"
        "Rules:\n"
        "- Operations allowed: addition, subtraction, multiplication, or division of fractions.\n"
        "- Denominators: use only 2, 3, 4, 5, 6, 8, or 10.\n"
        "- Answer must be a fraction or mixed number — never a decimal or whole number.\n"
        "- The problem must be solvable in at most 2 clear steps.\n"
        "- Distractors must be plausible fraction answers (wrong sign, wrong denominator, or "
        "common procedural errors) — not random numbers.\n\n"
        "For each problem provide exactly these keys:\n"
        "1. 'question': The word problem (one or two sentences, daily life theme).\n"
        "2. 'correct': The exact answer as a fraction string, e.g. '3/4' or '1 1/2'.\n"
        "3. 'distractors': A list of exactly 3 incorrect fraction answers.\n"
        "4. 'explanation': Two numbered steps showing the arithmetic.\n\n"
        "Example of ONE valid object:\n"
        "{\n"
        "  \"question\": \"A recipe calls for 3/4 of a cup of sugar. "
        "If you want to make 2 batches, how much sugar do you need in total?\",\n"
        "  \"correct\": \"1 1/2\",\n"
        "  \"distractors\": [\"3/8\", \"1 1/4\", \"2/4\"],\n"
        "  \"explanation\": \"Step 1: Multiply the fraction by the number of batches: 3/4 × 2 = 6/4. "
        "Step 2: Simplify 6/4 to the mixed number 1 2/4 = 1 1/2.\"\n"
        "}\n\n"
        "Return a JSON array of 5 such objects."
    )
    
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2048,
            system=system_instruction,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )

        raw_content = response.content[0].text

        # Use regex to find the JSON array in case the model adds conversational filler
        match = re.search(r'\[.*\]', raw_content, re.DOTALL)

        if match:
            data = json.loads(match.group())

            # Ensure output directory exists before saving
            os.makedirs("output", exist_ok=True)
            with open(DATA_FILE, "w") as f:
                json.dump(data, f)
            return data

    except Exception as e:
        print(f"Error fetching from Claude: {e}")
        
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
