import streamlit as st
import random

# --- PAGE SETUP ---
st.set_page_config(page_title="Sky Island Adventure", page_icon="☁️", layout="wide")

# --- MAGICAL THEME CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #87CEEB, #E0F7FA);
    }
    .island-card {
        background: white;
        padding: 20px;
        border-radius: 25px;
        text-align: center;
        border: 4px solid #fff;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.1);
    }
    .active-island {
        border: 4px solid #FFD700;
        background: #FFF9C4;
        box-shadow: 0px 0px 30px rgba(255, 215, 0, 0.6);
    }
    .player-avatar { font-size: 40px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- GAME STATE ---
ISLANDS = 25
if 'positions' not in st.session_state:
    st.session_state.positions = {"Noor ul Huda": 0, "Noor ul Ain": 0, "Hiba Fraz": 0}
    st.session_state.turn = 0
    st.session_state.event = "The sun is shining on the Sky Islands! ☀️"

players = ["Noor ul Huda", "Noor ul Ain", "Hiba Fraz"]
avatars = {"Noor ul Huda": "🦄", "Noor ul Ain": "🦋", "Hiba Fraz": "🌈"}
current_p = players[st.session_state.turn]

# --- UI HEADER ---
st.title("☁️ Sky Island Adventure")
st.write("### Leap across the floating islands to reach the Rainbow Castle!")

# --- PLAYER STATUS ---
cols = st.columns(3)
for i, p in enumerate(players):
    is_turn = "active-island" if p == current_p else ""
    with cols[i]:
        st.markdown(f"""
            <div class='island-card {is_turn}'>
                <div class='player-avatar'>{avatars[p]}</div>
                <h3>{p}</h3>
                <p>On Island: <b>{st.session_state.positions[p]}</b></p>
            </div>
        """, unsafe_allow_html=True)

st.write("---")

# --- GAMEPLAY ---
c1, c2, c3 = st.columns([1,2,1])
with c2:
    if st.button(f"✨ {current_p.upper()}, LEAP TO THE NEXT ISLAND!", use_container_width=True):
        jump = random.randint(1, 4) # Smaller jumps for more interaction
        st.session_state.positions[current_player] += jump
        
        # Check for Mystery Islands
        pos = st.session_state.positions[current_p]
        msg = f"{avatars[current_p]} {current_p} jumped {jump} islands!"
        
        # Surprise Events
        if pos in [5, 12, 18]:
            st.session_state.positions[current_p] += 3
            msg = f"🚀 WIND GUST! {current_p} flew 3 extra islands forward!"
        elif pos in [8, 15, 22]:
            st.session_state.positions[current_p] -= 2
            msg = f"☁️ FOGGY CLOUD! {current_p} got lost and went back 2 islands."
        elif pos == 10:
            msg = f"💎 MAGIC GEM! {current_p} found a gem and gets an extra turn!"
            st.session_state.event = msg
            st.rerun() # Skip the turn increment
            
        st.session_state.event = msg
        
        # Win Condition
        if st.session_state.positions[current_p] >= ISLANDS:
            st.balloons()
            st.success(f"👑 {current_p} HAS REACHED THE RAINBOW CASTLE!")
            st.session_state.positions = {k: 0 for k in st.session_state.positions}
        else:
            st.session_state.turn = (st.session_state.turn + 1) % 3
            st.rerun()

    st.info(st.session_state.event)

# --- VISUAL MAP ---
st.write("### 🗺️ The Map")
# We create a horizontal visual of the journey
track = ["⬜"] * (ISLANDS + 1)
for p in players:
    p_pos = min(st.session_state.positions[p], ISLANDS)
    track[p_pos] = avatars[p]

st.markdown(f"<h1 style='text-align: center;'>{' '.join(track)} 🏰</h1>", unsafe_allow_html=True)