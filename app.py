import streamlit as st
import random
import time

# --- ADVANCED UI CONFIG ---
st.set_page_config(page_title="Gem Hunters: The Sibling Quest", page_icon="💎", layout="wide")

# Custom CSS for Neon Luxury Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp { background-color: #0E1117; color: white; }
    
    .player-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 25px;
        border: 2px solid #30363D;
        text-align: center;
        transition: 0.3s;
    }
    .active-player {
        border: 2px solid #00D4FF;
        box-shadow: 0px 0px 20px rgba(0, 212, 255, 0.4);
        transform: scale(1.02);
    }
    .gem-count { font-family: 'Orbitron', sans-serif; font-size: 2.5rem; color: #00D4FF; }
    .dice-roll { font-size: 3rem; font-weight: bold; color: #FF007A; }
    </style>
    """, unsafe_allow_html=True)

# --- GAME ENGINE ---
WIN_SCORE = 30

if 'gems' not in st.session_state:
    st.session_state.gems = {"Noor ul Huda": 0, "Noor ul Ain": 0, "Hiba Fraz": 0}
if 'turn_idx' not in st.session_state:
    st.session_state.turn_idx = 0
if 'history' not in st.session_state:
    st.session_state.history = ["Game Started! Good luck hunters."]

players = list(st.session_state.gems.keys())
current_p = players[st.session_state.turn_idx]

# --- HEADER ---
st.markdown("<h1 style='text-align: center;'>💎 GEM HUNTERS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>First to collect 30 Gems wins the Golden Crown!</p>", unsafe_allow_html=True)

# --- GAME WORLD ---
col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]

for i, p in enumerate(players):
    is_active = "active-player" if p == current_p else ""
    with cols[i]:
        st.markdown(f"""
            <div class='player-card {is_active}'>
                <h2 style='margin-bottom:0;'>{p}</h2>
                <div class='gem-count'>{st.session_state.gems[p]}</div>
                <p style='color: #666;'>GEMS COLLECTED</p>
            </div>
            """, unsafe_allow_html=True)

st.divider()

# --- THE CONTROLS ---
left, mid, right = st.columns([1, 2, 1])

with mid:
    st.markdown(f"<h3 style='text-align: center;'>It is {current_p}'s Turn</h3>", unsafe_allow_html=True)
    
    if st.button("🎲 ROLL THE ANCIENT DICE", use_container_width=True):
        roll = random.randint(1, 6)
        
        # Logic for interesting events
        event_msg = ""
        if roll == 6:
            bonus = 2
            st.session_state.gems[current_p] += (roll + bonus)
            event_msg = f"✨ CRITICAL HIT! {current_p} found a hidden cache! (+{roll + bonus})"
        elif roll == 1:
            st.session_state.gems[current_p] += roll
            event_msg = f"🐍 Oh no! {current_p} slipped on a snake! (+1 only)"
        else:
            st.session_state.gems[current_p] += roll
            event_msg = f"💎 {current_p} found {roll} gems!"

        st.session_state.history.insert(0, event_msg)
        
        # Check Win Condition
        if st.session_state.gems[current_p] >= WIN_SCORE:
            st.balloons()
            st.snow()
            st.toast(f"VICTORY FOR {current_p}!", icon="🏆")
            st.session_state.winner = current_p
        else:
            st.session_state.turn_idx = (st.session_state.turn_idx + 1) % 3
            st.rerun()

# --- LOG & REWARDS ---
with st.sidebar:
    st.title("📜 Quest Log")
    for log in st.session_state.history[:5]:
        st.write(log)
    
    st.divider()
    if st.button("🔄 Reset Quest"):
        st.session_state.clear()
        st.rerun()

# --- CELEBRATION MODAL ---
if 'winner' in st.session_state:
    st.markdown(f"""
        <div style='background: #FFD700; padding: 50px; border-radius: 20px; text-align: center; color: black;'>
            <h1>👑 THE CROWN GOES TO {st.session_state.winner}! 👑</h1>
            <p>You are the Master Gem Hunter of 2025!</p>
        </div>
    """, unsafe_allow_html=True)