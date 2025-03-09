import streamlit as st
import random
from puzzles import puzzles, get_random_puzzles
import ai_hint
from dynamic_puzzle import generate_dynamic_puzzle
import time
import visual_clue

# Aestehtics, background, etc for the game
def set_background():
    st.set_page_config(
        page_title="Puzzle Quest",
        page_icon="🧩",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown(
        """
        <style>
        .stApp {
            background-image: linear-gradient(to bottom, #1a1a2e, #16213e);
            color: #ffffff;
        }
        .puzzle-card {
            background-color: rgba(0, 0, 0, 0.4);
            border-radius: 10px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-bottom: 20px;
        }
        .game-title {
            font-family: 'Courier New', monospace;
            text-align: center;
            color: #00f5d4;
            text-shadow: 0 0 10px rgba(0, 245, 212, 0.5);
        }
        .game-subtitle {
            font-family: 'Courier New', monospace;
            text-align: center;
            color: #00c9b7;
            margin-bottom: 30px;
        }
        .hint-text {
            font-style: italic;
            color: #ffd166;
        }
        .success-text {
            color: #06d6a0;
            font-weight: bold;
        }
        .error-text {
            color: #ef476f;
        }
        .game-button {
            background-color: #118ab2;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .game-button:hover {
            background-color: #073b4c;
        }
        .stats-box {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            padding: 10px;
            margin-top: 20px;
        }
        .stTextInput > div > div > input {
            background-color: rgba(0, 0, 0, 0.7);
            color: #ffde59;
            border: 2px solid rgba(255, 255, 255, 0.4);
            font-weight: bold;
            font-size: 16px;
            padding: 8px !important;
        }
        
        /* sidebar styles */
        .stSidebar {
            background-color: rgba(0, 0, 0, 0.85) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        p, span, label, div, h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
            text-shadow: 2px 2px 4px #000000 !important;
        }
        
        .stSidebar p, .stSidebar span, .stSidebar label, .stSidebar div {
            color: #ffde59 !important;
            text-shadow: 1px 1px 3px #000000 !important;
            font-weight: 500;
        }
        
        .stAlert {
            background-color: rgba(0, 0, 0, 0.85) !important;
            color: white !important;
            border: 2px solid rgba(255, 255, 255, 0.4) !important;
            border-radius: 8px !important;
        }
        
        .stSelectbox > div, .stRadio > div {
            background-color: rgba(0, 0, 0, 0.7) !important;
            border-radius: 8px !important;
            padding: 5px !important;
            border: 2px solid rgba(255, 255, 255, 0.3) !important;
        }
        
        .stSelectbox > div > div, .stRadio label {
            color: #ffde59 !important;
            font-weight: 500 !important;
        }
        
        .stats-box {
            background-color: rgba(0, 0, 0, 0.8) !important;
            border: 2px solid rgba(255, 255, 255, 0.3) !important;
        }
        
        .stExpander {
            background-color: rgba(0, 0, 0, 0.7) !important;
            border: 2px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 8px !important;
        }
        
        /* Button stylng */
        button {
            background-color: rgba(25, 60, 125, 0.9) !important;
            color: white !important;
            font-weight: bold !important;
            border: 2px solid rgba(255, 255, 255, 0.4) !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3) !important;
        }
        
        button:hover {
            background-color: rgba(45, 90, 160, 0.9) !important;
            transform: translateY(-2px) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def game_header():
    st.markdown('<h1 class="game-title">PUZZLE QUEST</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="game-subtitle">The Riddle King</h3>', unsafe_allow_html=True)

def custom_card(content, class_name="puzzle-card"):
    st.markdown(f'<div class="{class_name}">{content}</div>', unsafe_allow_html=True)

def main():
    set_background()
    game_header()
    
    # init session state vars just in case
    if 'puzzle_data' not in st.session_state:
        st.session_state.puzzle_data = None
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0
    if 'last_guess' not in st.session_state:
        st.session_state.last_guess = ""
    if 'solved' not in st.session_state:
        st.session_state.solved = False
    if 'total_puzzles_solved' not in st.session_state:
        st.session_state.total_puzzles_solved = 0
    if 'puzzles_seen' not in st.session_state:
        st.session_state.puzzles_seen = set()
    if 'streaks' not in st.session_state:
        st.session_state.streaks = 0
    if 'hints_used' not in st.session_state:
        st.session_state.hints_used = 0
    if 'game_start_time' not in st.session_state:
        st.session_state.game_start_time = time.time()
        
    # Sidebar for game settings and stats
    with st.sidebar:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://img.icons8.com/fluency/96/000000/puzzle.png", width=80)
        with col2:
            st.markdown("<h2 style='margin-top:10px;'>Enigma Quest</h2>", unsafe_allow_html=True)
        
        st.markdown("<hr style='margin:10px 0px; background-color:rgba(255,255,255,0.3); height:2px; border:none;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#ffde59;'>Game Settings</h3>", unsafe_allow_html=True)
        
        puzzle_type = st.radio("Puzzle Type:", ["Classic Riddles", "AI-Generated Riddles"])
        
        st.markdown("<h3 style='color:#ffde59; margin-top:20px;'>Player Stats</h3>", unsafe_allow_html=True)
        
        minutes = int((time.time() - st.session_state.game_start_time) / 60)
        hours = minutes // 60
        minutes = minutes % 60
        time_display = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        
        stats_content = f"""
        <div style='padding:10px; background-color:rgba(0,0,0,0.7); border-radius:10px; border:2px solid rgba(255,255,255,0.3);'>
            <div style='display:flex; justify-content:space-between; margin-bottom:10px;'>
                <span style='color:#ffde59;'>🏆 Puzzles Solved:</span>
                <span style='color:#ffffff; font-weight:bold;'>{st.session_state.total_puzzles_solved}</span>
            </div>
            <div style='display:flex; justify-content:space-between; margin-bottom:10px;'>
                <span style='color:#ffde59;'>🔥 Current Streak:</span>
                <span style='color:#ffffff; font-weight:bold;'>{st.session_state.streaks}</span>
            </div>
            <div style='display:flex; justify-content:space-between; margin-bottom:10px;'>
                <span style='color:#ffde59;'>💡 Hints Used:</span>
                <span style='color:#ffffff; font-weight:bold;'>{st.session_state.hints_used}</span>
            </div>
            <div style='display:flex; justify-content:space-between;'>
                <span style='color:#ffde59;'>⏱️ Game Time:</span>
                <span style='color:#ffffff; font-weight:bold;'>{time_display}</span>
            </div>
        </div>
        """
        st.markdown(stats_content, unsafe_allow_html=True)
        
        # basic how to play section
        with st.expander("How to Play"):
            st.markdown("""
            <div style='background-color:rgba(0,0,0,0.6); padding:15px; border-radius:8px;'>
                <ol style='margin-left:20px; padding-left:0px;'>
                    <li style='margin-bottom:8px; color:#ffde59;'>Read the riddle carefully</li>
                    <li style='margin-bottom:8px; color:#ffde59;'>Type your answer in the text box</li>
                    <li style='margin-bottom:8px; color:#ffde59;'>Click "Submit" to check if you're right</li>
                    <li style='margin-bottom:8px; color:#ffde59;'>Need help? Click "Get Hint" for a clue at the price of a guess</li>
                    <li style='color:#ffde59;'>Challenge yourself to solve as many riddles as possible!</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
    
    # classic puzzle where user gets a pre-made riddle 
    if puzzle_type == "Classic Riddles":
        selection_method = st.sidebar.radio(
            "Puzzle Selection",
            ["Choose a Specific Riddle", "Random Riddle"]
        )
        
        if selection_method == "Choose a Specific Riddle": # user can choose their own pre set riddle
            selected = st.sidebar.selectbox(
                "Choose a puzzle:",
                puzzles,
                format_func=lambda p: f"Riddle {p.id}: {p.question[:30]}..."
            )
            # Update session state if diff puzzle is selected
            if (st.session_state.puzzle_data is None) or (st.session_state.puzzle_data.get("id") != selected.id):
                st.session_state.puzzle_data = {
                    "id": selected.id,
                    "question": selected.question,
                    "answer": selected.answer,
                    "context": selected.context
                }
                st.session_state.attempts = 0
                st.session_state.last_guess = ""
                st.session_state.solved = False
                if selected.id not in st.session_state.puzzles_seen:
                    st.session_state.puzzles_seen.add(selected.id)
        else: # give random riddle if they choose iout of the preset ones
            if st.sidebar.button("Get Random Riddle"):
                random_puzzle = random.choice(get_random_puzzles(list(st.session_state.puzzles_seen)))
                st.session_state.puzzle_data = {
                    "id": random_puzzle.id,
                    "question": random_puzzle.question,
                    "answer": random_puzzle.answer,
                    "context": random_puzzle.context
                }
                st.session_state.attempts = 0
                st.session_state.last_guess = ""
                st.session_state.solved = False
                if random_puzzle.id not in st.session_state.puzzles_seen:
                    st.session_state.puzzles_seen.add(random_puzzle.id)
    else: # Dynamic Puzzle option: gen new puzzle with ai if button is pressed
        if st.sidebar.button("Generate New Riddle"):
            with st.sidebar:
                with st.spinner("Creating a mysterious riddle..."):
                    generated = generate_dynamic_puzzle()
                    if generated:
                        st.session_state.puzzle_data = generated
                        st.session_state.attempts = 0
                        st.session_state.last_guess = ""
                        st.session_state.solved = False
                        st.success("New riddle awaits you!")
                    else:
                        st.error("The mystical powers failed. Try again.")
        if st.session_state.puzzle_data is None:
            st.info("Click the 'Generate New Riddle' button in the sidebar to get started on your quest.")
            return
        
    # Display the current riddle and input area
    puzzle_data = st.session_state.puzzle_data
    if not puzzle_data:
        st.info("Select a puzzle to begin your adventure!")
        return
    
    puzzle_content = f"""
    <div style='background: rgba(0, 0, 0, 0.7); padding: 25px; border-radius: 15px; border: 3px solid rgba(255, 222, 89, 0.5); box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);'>
        <h2 style='color: #ffde59; text-align: center; margin-bottom: 15px; text-shadow: 2px 2px 4px #000000;'>Riddle #{puzzle_data.get('id', random.randint(100, 999))}</h2>
        <div style='font-size: 20px; color: white; text-align: center; font-style: italic; text-shadow: 2px 2px 4px #000000;'>
            "{puzzle_data['question']}"
        </div>
    </div>
    """
    st.markdown(puzzle_content, unsafe_allow_html=True)
    
    # attempts and streaks display
    if st.session_state.attempts > 0:
        attempt_text = "attempt" if st.session_state.attempts == 1 else "attempts"
        
        cols = st.columns(5)
        for i in range(5):
            if i < st.session_state.attempts:
                color = "#ef476f" if i >= 3 else "#ffd166"
                cols[i].markdown(f"<div style='background-color: {color}; height: 10px; border-radius: 5px; margin: 5px;'></div>", unsafe_allow_html=True)
            else:
                cols[i].markdown("<div style='background-color: rgba(255,255,255,0.2); height: 10px; border-radius: 5px; margin: 5px;'></div>", unsafe_allow_html=True)
        
        st.markdown(f"<div style='text-align: center; margin-bottom: 20px; color: #ffd166;'>{st.session_state.attempts} {attempt_text} so far</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='background-color: rgba(0,0,0,0.5); padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 2px solid rgba(255,255,255,0.3);'>", unsafe_allow_html=True)
    
    # Input area for the answer
    col1, col2 = st.columns([3, 1])
    with col1:
        if not st.session_state.solved:
            answer = st.text_input("", key="answer_input", 
                                   placeholder="Enter your answer here...",
                                   label_visibility="collapsed")
        else:
            answer = st.session_state.last_guess
            st.markdown(f"<div style='padding: 10px; background-color: rgba(0,0,0,0.7); color: #06d6a0; border-radius: 5px;'>Your answer: <b>{answer}</b></div>", unsafe_allow_html=True)
    
    with col2:
        if not st.session_state.solved and st.button("Submit", key="submit_btn", use_container_width=True):
            if not answer.strip():
                st.warning("Please enter an answer first!")
            else:
                st.session_state.attempts += 1
                st.session_state.last_guess = answer.strip()
                if answer.strip().lower() == puzzle_data["answer"].lower():
                    st.session_state.solved = True
                    st.session_state.total_puzzles_solved += 1
                    st.session_state.streaks += 1
                    st.balloons()
                    st.success("🎉 Congratulations! You've solved the riddle! 🎉")
                    
                    # celebratory message
                    if st.session_state.streaks > 1:
                        st.markdown(f"<div style='text-align: center; padding: 10px; background-color: rgba(0,0,0,0.7); color: #ffde59; border-radius: 5px; margin-top: 10px;'>🔥 You're on a streak of {st.session_state.streaks} riddles! 🔥</div>", unsafe_allow_html=True)
                else:
                    st.error("That's not the answer. Try again!")
                    st.session_state.streaks = 0
    
    st.markdown("</div>", unsafe_allow_html=True)
 
    st.markdown("<div style='margin: 20px 0;'>", unsafe_allow_html=True)
    response_container = st.container()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='display: flex; justify-content: space-between; margin-top: 20px;'>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4) 
    
    # Hint, visual clue, and answer reveal buttons
    with col1:
        if st.button("💡 Get Hint", use_container_width=True, 
                    help="Get a mysterious hint to guide you toward the answer at the cost of one guess"):
            if not st.session_state.solved:
                st.session_state.hints_used += 1
                st.session_state.attempts += 1
                attempts = st.session_state.attempts
                hint_request = f"attempted {attempts} time(s) unsuccessfully"
                last_guess = st.session_state.last_guess if st.session_state.last_guess else None
                
                with response_container:
                    with st.spinner("The oracle is consulting the ancient scrolls..."):
                        hint_message = ai_hint.generate_hint(puzzle_data["context"], hint_request, attempts, last_guess, puzzle_data["answer"])
                        
                        # Display hint in a styled container
                        st.markdown(f"""
                        <div style='background-color: rgba(0, 0, 0, 0.7); padding: 15px; border-radius: 10px; border: 2px solid #ffd166;'>
                            <div style='font-weight: bold; margin-bottom: 8px; color: #ffd166;'>The Oracle speaks:</div>
                            <div style='font-style: italic; color: #ffffff;'>{hint_message}</div>
                        </div>
                        """, unsafe_allow_html=True)

    with col2:
        if st.button("🎨 Visual Clue", use_container_width=True,
                    help="Receive a mystical image that may guide you to the answer"):
            if not st.session_state.solved:
                st.session_state.hints_used += 1
                st.session_state.attempts += 1
                
                with response_container:
                    visual_clue.display_visual_clue(
                        st, 
                        puzzle_data["question"], 
                        puzzle_data["answer"],
                        difficulty=min(st.session_state.attempts, 3)  # # attempts ifluences difficulty so pass
                    )
        
    with col3:
        if st.button("🔍 Reveal Answer", use_container_width=True,
                    help="Show the answer, but you'll lose your streak!"):
            with response_container:
                st.markdown(f"""
                <div style='background-color: rgba(0, 0, 0, 0.7); padding: 15px; border-radius: 10px; border: 2px solid #ef476f;'>
                    <div style='font-weight: bold; margin-bottom: 8px; color: #ef476f;'>The mystery is revealed:</div>
                    <div style='font-size: 18px; text-align: center; color: #ffffff;'>The answer is <span style='color: #ef476f; font-weight: bold;'>{puzzle_data['answer']}</span></div>
                    <div style='font-size: 12px; text-align: center; margin-top: 10px; color: #ffd166;'>Your streak has been reset</div>
                </div>
                """, unsafe_allow_html=True)
                st.session_state.streaks = 0
    
    with col4:
        if st.button("➡️ Next Puzzle", use_container_width=True,
                    help="Move to a new riddle challenge. For static, look through the left sidebar."):
            # dynamic puzzles generate a new puzzle
            if puzzle_type == "AI-Generated Riddles":
                with st.spinner("Creating another riddle..."):
                    new_puzzle = generate_dynamic_puzzle()
                    if new_puzzle:
                        st.session_state.puzzle_data = new_puzzle
                    else:
                        st.error("Failed to generate a new riddle.")
                        return
            else:
                # For static puzzles, get a random unseen puzzle, or nothing if its not the random selection.
                unseen_puzzles = get_random_puzzles(list(st.session_state.puzzles_seen))
                if unseen_puzzles:
                    random_puzzle = random.choice(unseen_puzzles)
                    st.session_state.puzzle_data = {
                        "id": random_puzzle.id,
                        "question": random_puzzle.question,
                        "answer": random_puzzle.answer,
                        "context": random_puzzle.context
                    }
                    if random_puzzle.id not in st.session_state.puzzles_seen:
                        st.session_state.puzzles_seen.add(random_puzzle.id)
                else:
                    random_puzzle = random.choice(puzzles)
                    st.session_state.puzzle_data = {
                        "id": random_puzzle.id,
                        "question": random_puzzle.question,
                        "answer": random_puzzle.answer,
                        "context": random_puzzle.context
                    }
            
            # Reset state values for new puzzle
            st.session_state.attempts = 0
            st.session_state.last_guess = ""
            st.session_state.solved = False
        
            st.query_params.update({
                "refresh": str(random.random())
            })  
            st.rerun()

if __name__ == '__main__':
    main()