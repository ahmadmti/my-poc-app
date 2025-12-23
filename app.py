import streamlit as st
import random

# --- CONFIG ---
st.set_page_config(page_title="Jungle Safari Adventure", page_icon="🦁", layout="wide")

# --- CUSTOM JUNGLE THEME ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f0fdf4;
    }
    .player-card {
        padding: 15px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        border: 4px solid transparent;
    }
    .active { border-color: #16a34a; background-color: #dcfce7; transform: scale(1.05); }
    .stat-text { font-size: 24px; font-weight: bold; color: #16a34a; }
    .jungle-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 2px dashed #16a34a;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GAME SETUP ---
GOAL = 30
if 'scores' not in st.session_state:
    st.session_state.scores = {"Noor ul Huda 🦁": 0, "Noor ul Ain 🦒": 0, "Hiba Fraz 🐘": 0}
    st.session_state.turn = 0
    st.session_state.log = "Welcome to the Jungle! 🌴"

players = list(st.session_state.scores.keys())
current_player = players[st.session_state.turn]

# --- UI LAYOUT ---
st.title("🌴 The Magic Jungle Safari")
st.write("### First one to reach the Golden Banana (30 steps) wins!")

# Top Row: Player Cards
cols = st.columns(3)
for i, name in enumerate(players):
    is_active = "active" if name == current_player else ""
    with cols[i]:
        st.markdown(f"""
            <div class='player-card {is_active}'>
                <h2>{name}</h2>
                <p class='stat-text'>{st.session_state.scores[name]} / {GOAL}</p>
                <p>Steps Taken</p>
            </div>
        """, unsafe_allow_html=True)

st.write("##")

# Middle Row: The Dice and Event
c1, c2, c3 = st.columns([1,2,1])
with c2:
    st.markdown("<div class='jungle-box'>", unsafe_allow_html=True)
    if st.button(f"🎲 ROLL DICE FOR {current_player.upper()}", use_container_width=True):
        roll = random.randint(1, 6)
        
        # Jungle Events
        event_roll = random.random()
        bonus = 0
        event_msg = f"{current_player} rolled a {roll}!"
        
        if event_roll > 0.8: # 20% chance of an animal event
            event_type = random.choice(["Monkey", "Snake", "Cheetah"])
            if event_type == "Monkey":
                bonus = 3
                event_msg = f"🐒 A Monkey gave {current_player} a lift! (+3 extra steps)"
            elif event_type == "Snake":
                bonus = -2
                event_msg = f"🐍 Oh no! A Snake scared {current_player}! (Go back 2 steps)"
            elif event_type == "Cheetah":
                bonus = 5
                event_msg = f"🐆 WOW! A Cheetah sprint! (+5 extra steps)"
        
        # Update Score
        st.session_state.scores[current_player] = max(0, st.session_state.scores[current_player] + roll + bonus)
        st.session_state.log = event_msg
        
        # Check Winner
        if st.session_state.scores[current_player] >= GOAL:
            st.balloons()
            st.success(f"🏆 {current_player} FOUND THE GOLDEN BANANA AND WINS!")
            st.session_state.scores = {k: 0 for k in st.session_state.scores} # Reset
        else:
            st.session_state.turn = (st.session_state.turn + 1) % 3
            st.rerun()
            
    st.markdown(f"### {st.session_state.log}")
    st.markdown("</div>", unsafe_allow_html=True)

# Bottom: Visual Progress
st.write("##")
for name in players:
    score = st.session_state.scores[name]
    st.write(f"**{name}**")
    st.progress(min(score/GOAL, 1.0))