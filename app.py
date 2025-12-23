import streamlit as st
import random

# --- CONFIG ---
st.set_page_config(page_title="The Sibling Race", page_icon="🏁")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .player-box { padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #ddd; }
    .noor-huda { background-color: #FFEBEE; border-color: #FF5252; }
    .noor-ain { background-color: #E8F5E9; border-color: #4CAF50; }
    .hiba { background-color: #E3F2FD; border-color: #2196F3; }
    .finish-line { background-color: #FFF9C4; border: 2px dashed #FBC02D; padding: 10px; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- GAME LOGIC ---
GOAL = 20

# Initialize Game State
if 'pos' not in st.session_state:
    st.session_state.pos = {"Noor ul Huda": 0, "Noor ul Ain": 0, "Hiba Fraz": 0}
if 'turn' not in st.session_state:
    st.session_state.turn = 0
if 'winner' not in st.session_state:
    st.session_state.winner = None

players = ["Noor ul Huda", "Noor ul Ain", "Hiba Fraz"]
current_player = players[st.session_state.turn]

# --- UI ---
st.title("🏁 The Great Sibling Race")
st.write(f"First to reach **{GOAL}** steps wins!")

if not st.session_state.winner:
    st.subheader(f"👉 It's {current_player}'s Turn!")
    
    if st.button(f"🎲 Roll Dice for {current_player}"):
        roll = random.randint(1, 6)
        st.session_state.pos[current_player] += roll
        st.write(f"**{current_player}** rolled a **{roll}**!")
        
        # Check for winner
        if st.session_state.pos[current_player] >= GOAL:
            st.session_state.winner = current_player
        else:
            # Move to next player
            st.session_state.turn = (st.session_state.turn + 1) % 3
            st.rerun()

# --- THE TRACK (Visual Representation) ---
st.divider()

for p in players:
    # Set style based on player
    style_class = "noor-huda" if "Huda" in p else "noor-ain" if "Ain" in p else "hiba"
    
    # Progress bar and visual markers
    score = st.session_state.pos[p]
    progress = min(score / GOAL, 1.0)
    
    st.markdown(f"<div class='player-box {style_class}'>", unsafe_allow_html=True)
    st.write(f"### {p}")
    st.progress(progress)
    st.write(f"Steps: **{score}** / {GOAL}")
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("")

# --- WINNER SECTION ---
if st.session_state.winner:
    st.balloons()
    st.success(f"🏆 CONGRATULATIONS! {st.session_state.winner} WINS!")
    if st.button("🔄 Play Again"):
        st.session_state.pos = {"Noor ul Huda": 0, "Noor ul Ain": 0, "Hiba Fraz": 0}
        st.session_state.turn = 0
        st.session_state.winner = None
        st.rerun()

st.divider()
st.markdown("<div class='finish-line'>🏁 FINISH LINE (Step 20)</div>", unsafe_allow_html=True)