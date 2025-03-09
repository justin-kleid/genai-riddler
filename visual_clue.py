import os
import openai
from dotenv import load_dotenv
import base64
import requests
from PIL import Image
from io import BytesIO

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

# Generate a visual clue for a riddle based off riddle, answer, and difficulty
def generate_visual_clue(riddle, answer, difficulty=1):
    if difficulty == 1:
        subtlety = "subtle and abstract"
    elif difficulty == 2:
        subtlety = "somewhat abstract but with recognizable elements"
    else:
        subtlety = "containing symbolic elements that hint at the answer"
    
    prompt = (
        f"Create a {subtlety} visual clue for a riddle. "
        f"The riddle is: '{riddle}' and the answer is '{answer}'. "
        f"The image should hint at the answer without making it too obvious. "
        f"Do not include any text or letters in the image. "
        f"Make the image symbolic not too literal (e.g. for a footprint do a boot not a footprint)."
    )
    
    try:
        # Call the DALL-E API
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        
        image_url = response['data'][0]['url']
        
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        
        return image
        
    except Exception as e:
        print(f"Error visual clue: {e}")
        return None

# add visual clue to Streamlit app
def display_visual_clue(st, riddle, answer, difficulty=1):
    with st.spinner("The mystical artist is creating a visual clue..."):
        image = generate_visual_clue(riddle, answer, difficulty)
        
        if image:
            st.image(image, caption="A mystical visual clue", use_container_width=True)
        else:
            st.warning("The mystical artist could not create a visual clue at this time.")