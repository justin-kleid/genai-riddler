## Overview of Puzzle Quest

This project is a riddle game using simple traditional puzzles with AI twists.


### Features

This project functions as a game-like puzzle generator. It runs on streamlit, and the UI and mechanics are
extremely gamified.

Users select between classic riddles, which are pre-written (via some internet research and normal AI generation i.e. asking ChatGPT, Deepseek, etc)
and common puzzles. For this puzzle type, users can either choose a specific riddle out of a dropdown or a random one out of the 20 created.
In these puzzles, the user can put in a guess, get a hint or viusal clue, or reveal the answer.

As users guess wrong or use hints, a progress bar tracks their progress, turning red as they get too many guesses wrong. These stats are also 
tracked in the Player Stats sidebar with thier minutes played, hints used, puzzles solved, and current puzzle streak. 

The other puzzle type is AI-Generated Puzzles. ChatGPT 4o is queried with a list of general riddle themes (with one being chosen at random)
for each puzzle. The user can then do the same actions as with the static puzzle type or choose to generate a new puzzle.

The game is not fully comprehensive and is still in a demo-like state. There are subtle bugs such as the guess counter not triggering on the first hint or
if the random riddle is spammed more than 20 times (as there are only 20 puzzles). While in a real customer facing deployment, these issues would definitely need to
be resolved, the focus of this repo is more on the game and AI integrated logic.

### AI Integrations

For both puzzle types, the user can get AI hints or visual clues. These heavily rely on prompt engineering tactics.
For example, contextual framing is key for giving the mystical theme of the game (i.e. an oracle giving mysterious hints rather 
than boring, explicit ones). Another big use case was to stop the ChatGPT 4o model from just giving the answer in the hints, and so I had
to give it avoid instructions that they would not say. As in previous assignments, formatting the AI responses (e.g. as a JSON with certain keys)
was also important.

Besides the basic context and prompt engineerning tactics, I gave the model a more intelligent seeming hint system. First of all, if the player guesses,
their previous guess is passed into the model so that it can provide relevant clues, e.g. right track or not. The difficulty also scales based on the 
number of guesses, which is passed into the model, with more clear hints being given later on.

The other hints are visual hints, which are a little more hit and miss than the textual ones but still a fun feature. This uses DALL-E api to make images
that will hint towards the answer. I tried a lot of different prompt engineering to guide the images in certain ways but I found this was the hardest element to 
control in the project. The successes are that the model could create images that kept the mysterious vibe of the project with the
same difficulty scaling. However, despite giving it advice on not 
being too obvious or too cryptic, sometimes the model would generate images that are literally the answer or absurdly abstract. Still, as a player, it was pretty
fun to try to decipher some of the hints.

e.g.

Riddle #139 (ai gen-ed)
"I come once in a minute, twice in a moment, but never in a thousand years. What am I?" ANSWER = m (the letter)

<img width="834" alt="Screenshot 2025-03-09 at 3 04 52 PM" src="https://github.com/user-attachments/assets/3c7d08ce-d8f7-44d8-8d77-91bf50324748" />

I kept getting strange images like this and I slowly realized they all had a letter integrated in them in some abstract way, which I thought was actually
pretty cool.


Finally, the last big AI use was the actual AI generated riddles. This mostly relied on prompt engineering as the gpt 4o loves to give one riddle about 
echoes almost everytime (spoiler: this is puzzle #1 in the static puzzles). To combat this, I told it to avoid common riddles such as ones about echoes, footsteps, etc
as well as it giving it a set of themes to choose from randomly each time. This helped a lot. For all of the AI stuff, there are fallback riddles but as long as the API
is working, it should not be triggered. Also, all of these uses required strict parameter enforcement such as making sure the answer to the generated hint would only be one word.

Differernt integrations also used different temperatures in this vein. I used 0.8 for riddle generation for more creativity, 0.7 for hint generation so it is a bit more grounded, etc.

### Technologies

Dall-E, gpt 4o, and streamlit

### Running the project

#### clone repo
``git clone https://github.com/justin-kleid/genai-riddler.git``
``cd genai-riddler``

#### venv for mac (can also do w/out an environment or your preferred method)
``python -m venv riddlenv``
``source riddlenv/bin/activate``
``pip install -r requirements.txt``

#### make env file with api key
``echo "OPENAI_API_KEY=put_in_api_key_here" > .env``

#### run app
``streamlit run app.py``

