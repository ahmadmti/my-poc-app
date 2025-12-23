import streamlit as st
import time

# --- CONFIG ---
st.set_page_config(page_title="Happy New Year Hiba!", page_icon="🎁", layout="wide")

# --- FESTIVE CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url('https://images.unsplash.com/photo-1467810563316-b5476525c0f9?auto=format&fit=crop&q=80&w=1200');
        background-size: cover;
        color: #D4AF37;
    }
    .gift-text { font-family: 'Playfair Display', serif; text-align: center; }
    .stButton>button { 
        background: linear-gradient(45deg, #D4AF37, #F9F295); 
        color: black; 
        font-weight: bold; 
        border-radius: 50px; 
        border: none;
        padding: 10px 40px;
    }
    .card {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #D4AF37;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
page = st.sidebar.selectbox("Navigate:", ["The Reveal", "Year in Review", "New Year Wishes"])

# --- PAGE 1: THE REVEAL ---
if page == "The Reveal":
    st.markdown("<h1 class='gift-text'>Happy New Year, Hiba Fraz! ✨</h1>", unsafe_allow_html=True)
    st.write("##")
    
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/4213/4213958.png", width=200)
        st.write("### A special gift is waiting for you...")
        
        if st.button("🎁 OPEN YOUR GIFT"):
            st.balloons()
            st.snow()
            st.success("### Surprise! You have a ticket to a wonderful 2026!")
            st.write("May this year bring you endless happiness, success, and beautiful moments.")
            st.image("https://images.unsplash.com/photo-1513151233558-d860c5398176?auto=format&fit=crop&q=80&w=800")
        st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 2: YEAR IN REVIEW ---
elif page == "Year in Review":
    st.title("Reflecting on 2025")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Your Achievements")
        st.info("⭐ Mastered New Tech Skills")
        st.info("⭐ Built Amazing POCs")
        st.info("⭐ Inspired Everyone Around You")
    
    with col_b:
        st.subheader("Memorable Moments")
        # You can replace these with actual photo URLs later
        st.image("https://images.unsplash.com/photo-1521478413868-1bbd8195f386?auto=format&fit=crop&q=80&w=400", caption="Joyful Times")

# --- PAGE 3: NEW YEAR WISHES ---
elif page == "New Year Wishes":
    st.title("Write Your 2026 Resolutions")
    
    with st.container():
        res1 = st.text_input("What is your #1 Goal for 2026?")
        res2 = st.text_input("What is one thing you want to learn?")
        
        if st.button("Save Resolutions"):
            st.write("### 📝 Your 2026 Vision Board:")
            st.write(f"1. **Primary Goal:** {res1}")
            st.write(f"2. **Learning Path:** {res2}")
            st.toast("Resolutions locked in! You've got this, Hiba!", icon="🔥")

# --- FOOTER ---
st.write("---")
st.markdown("<p style='text-align: center;'>Made with ❤️ for Hiba Fraz | Cheers to 2026</p>", unsafe_allow_html=True)