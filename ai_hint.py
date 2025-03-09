import os
import openai
from dotenv import load_dotenv
import random

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

# Fallback hints if API access fails (working fine w/out)
FALLBACK_HINTS = [
    "Look at the first letter of each word in the riddle.",
    "Try thinking about everyday objects that could fit the description.",
    "Consider metaphorical rather than literal interpretations.",
    "Sometimes the answer is hiding in plain sight within the riddle itself.",
    "Think of objects that share multiple characteristics mentioned in the riddle.",
    "Consider wordplay or puns that might be relevant.",
    "The answer might be something very common that you interact with daily.",
    "Try to visualize what the riddle is describing.",
    "Break down the riddle into smaller parts and solve each part.",
    "Think outside the box - the answer might be something unexpected."
]

# generate a hint for the player based on the puzzle context, hint request, last guess and current attempt
# number, varying on quality.
def generate_hint(puzzle_context, hint_request, attempt, last_guess=None, answer=None):
    """
    - puzzle_context: Description of the puzzle/riddle
    - hint_request: Description of the player's struggle
    - attempt: Current attempt count
    - last_guess: The player's last incorrect answer
    - answer: The actual answer to the riddle (used to ensure hint doesn't reveal it)
    """
    
    # avoid giving answer in plural form ,etc
    avoid_words = []
    if answer:
        avoid_words = [answer.lower()]
        if not answer.endswith('s'):
            avoid_words.append(f"{answer}s")
        if answer.endswith('s'):
            avoid_words.append(answer[:-1])
    
    avoid_instruction = ""
    if avoid_words:
        avoid_instruction = f"NEVER use these words in your hint: {', '.join(avoid_words)}. "

    # How useful hint is style based on attempts
    if attempt <= 1:
        style = "subtle and cryptic"
    elif attempt <= 3:
        style = "moderately revealing"
    else:
        style = "strong but not giving away the full answer"
    
    # use last guess in answer if available
    guess_feedback = ""
    if last_guess:
        guess_feedback = f"The player's last guess was '{last_guess}'. "
        guess_feedback += "If this guess is on the right track, encourage them. If not, gently redirect them. "
    
    #  game-like prompt w oracle
    prompt = (
        f"You are the Oracle, a mystical guide in a riddle game. The current riddle is about: {puzzle_context}. "
        f"{guess_feedback}"
        f"A player has {hint_request}. "
        f"{avoid_instruction}"
        f"Provide a {style} hint that helps them solve the riddle without giving away the answer completely. "
        f"IMPORTANT: NEVER mention the actual answer or anything too close to it in your hint. "
        f"Keep your hint under 30 words, mysterious in tone, and engaging like you're in a fantasy game setting. "
        f"Focus on helping them understand the riddle's concept rather than just giving direct clues. "
        f"Avoid using words that are similar to the answer or that would make the answer too obvious."
    )
    
    try:
        # try with modesl
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # GPT-4 first
                messages=[{"role": "user", "content": prompt}],
                max_tokens=60,
                temperature=0.7
            )
        except:
            # Fall back to GPT-3.5
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=60,
                temperature=0.7
            )
            
        hint = response.choices[0].message['content'].strip()
        hint_symbols = ["✨", "🔮", "🧙", "📜", "⚡", "🧠", "🗝️", "🌟", "🧩", "💭"]
        random_symbol = random.choice(hint_symbols)
        
        return f"{random_symbol} {hint}"
    
    except Exception as e:
        print(f"Error gen hint via API: {e}")
        # Fall back to pre-written if API fails
        fallback_hint = random.choice(FALLBACK_HINTS)
        return f"🧙 {fallback_hint}"