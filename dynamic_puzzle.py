import json
import openai
import random
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Fallback riddles
FALLBACK_RIDDLES = [
    {
        "question": "I am not alive, but I can die. I don't have lungs, but I need air. I have no mouth, but water kills me. What am I?",
        "answer": "fire",
        "context": "A riddle about an element that exhibits life-like qualities."
    },
    {
        "question": "The more you fill me, the lighter I become. What am I?",
        "answer": "balloon",
        "context": "A riddle about an object that gets lighter as it's filled with a substance lighter than air."
    },
    {
        "question": "I'm tall when I'm young, and I'm short when I'm old. What am I?",
        "answer": "candle",
        "context": "A riddle about something that changes height as it's used up."
    },
    {
        "question": "I have branches, but no fruit, trunk, or leaves. What am I?",
        "answer": "bank",
        "context": "A riddle about an institution with branches that aren't related to trees."
    },
    {
        "question": "What can fill a room but takes up no space?",
        "answer": "light",
        "context": "A riddle about something intangible that can fill an area."
    }
]

# Themes for riddles to guide the AI gen
RIDDLE_THEMES = [
    "Nature and elements",
    "Everyday objects",
    "Abstract concepts",
    "Celestial bodies",
    "Food and drinks",
    "Animals and creatures",
    "Technology",
    "Time and seasons",
    "Geography and places",
    "Body parts"
]

# Generate a dynamic riddle based on a theme
def generate_dynamic_puzzle():
    theme = random.choice(RIDDLE_THEMES)
    
    prompt = (
        f"Create an original, clever riddle on the theme of '{theme}' with a single-word answer. "
        "The riddle should be challenging but fair, and should not rely on obscure knowledge. "
        "Avoid common riddles like those about echoes, footsteps, keyboards, etc. "
        "Format your response ONLY as a valid JSON object with these exact keys: "
        "'question' (the riddle text), 'answer' (one word, lowercase), and 'context' (brief explanation of the answer). "
        "Do not include any text outside the JSON object."
    )
    
    try:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.8
            )
        except:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.8
            )
        
        content = response.choices[0].message['content'].strip()
        
        try:
            puzzle_data = json.loads(content)
            
            # Validate the puzzle data
            required_keys = ['question', 'answer', 'context']
            if not all(key in puzzle_data for key in required_keys):
                raise ValueError("Response missing required keys")
            
            puzzle_data['answer'] = puzzle_data['answer'].lower().strip()
            if ' ' in puzzle_data['answer']:
                puzzle_data['answer'] = puzzle_data['answer'].split()[0]  # just make it one word
            
            return puzzle_data
                
        except json.JSONDecodeError:
            print("JSON parse error.  extract JSON substring.")
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = content[start:end]
                try:
                    puzzle_data = json.loads(json_str)
                    return puzzle_data
                except:
                    raise ValueError("Failed  extract valid JSON")
            else:
                raise ValueError("No valid JSON found")
                
    except Exception as e:
        print(f"Error w dynamic puzzle: {e}")
        return random.choice(FALLBACK_RIDDLES)