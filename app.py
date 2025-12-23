import streamlit as st
import pandas as pd
import sqlite3

# --- DATABASE SETUP (For Contact/Messages) ---
def init_db():
    conn = sqlite3.connect("noor_records.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, email TEXT, message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

# --- UI/UX CONFIG (Abark-Inspired) ---
st.set_page_config(page_title="Noor ul Huda | Official", page_icon="✨", layout="wide")

# Custom CSS for Minimalist Dark/Modern Aesthetic
st.markdown("""
    <style>
    /* Dark background like modern tech sites */
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    /* Elegant Typography */
    h1, h2 { font-family: 'Inter', sans-serif; font-weight: 800; letter-spacing: -1px; }
    p { color: #A0A0A0; font-size: 1.1rem; line-height: 1.6; }
    
    /* Clean Buttons */
    .stButton>button { 
        background-color: #FFFFFF; 
        color: #000000; 
        border-radius: 2px; 
        font-weight: bold; 
        border: none;
        padding: 0.5rem 2rem;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #E0E0E0; color: #000000; }
    
    /* Service/Feature Boxes */
    .info-card { 
        background-color: #161B22; 
        padding: 2rem; 
        border-radius: 8px; 
        border: 1px solid #30363D;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAV ---
st.sidebar.markdown("### 🧭 Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Portfolio", "Contact"])

# --- PAGE 1: HOME (ABARK STYLE HERO) ---
if page == "Home":
    # Empty space for top margin
    st.write("##")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("# NOOR UL HUDA")
        st.markdown("### *Visionary. Learner. Future Leader.*")
        st.write(
            "Welcome to the official digital space of Noor ul Huda. "
            "Dedicated to excellence, continuous growth, and building "
            "meaningful solutions for tomorrow."
        )
        if st.button("Explore Work"):
            st.info("Scroll down or use the sidebar to view the portfolio.")
            
    with col2:
        # Placeholder for a professional portrait or abstract tech art
        st.image("https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&q=80&w=800", caption="Innovating through technology")

    st.write("---")
    
    # Values/Features Section
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='info-card'><h3>Creative Design</h3><p>Focusing on aesthetics that inspire and engage users across all digital platforms.</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='info-card'><h3>Strategic Thinking</h3><p>Approaching problems with a data-driven mindset to find the most efficient paths.</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='info-card'><h3>Global Impact</h3><p>Building projects with a focus on scalability and positive societal contribution.</p></div>", unsafe_allow_html=True)

# --- PAGE 2: PORTFOLIO ---
elif page == "Portfolio":
    st.title("Selected Works")
    st.write("A showcase of projects, achievements, and milestones.")
    
    # Grid of Projects
    p1, p2 = st.columns(2)
    with p1:
        st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=600")
        st.markdown("#### Project Alpha: Data Analytics")
        st.write("Developing insights through modern visualization techniques.")
        
    with p2:
        st.image("https://images.unsplash.com/photo-1522542550221-31fd19575a2d?auto=format&fit=crop&q=80&w=600")
        st.markdown("#### Project Beta: Web Architecture")
        st.write("Building high-performance web systems using scalable technologies.")

# --- PAGE 3: CONTACT ---
elif page == "Contact":
    st.title("Get In Touch")
    st.write("Have a project in mind or just want to say hello?")
    
    contact_col, info_col = st.columns([2, 1])
    
    with contact_col:
        with st.form("contact_form"):
            u_name = st.text_input("Name")
            u_email = st.text_input("Email")
            u_msg = st.text_area("Message")
            
            if st.form_submit_button("Send Message"):
                if u_name and u_msg:
                    conn = sqlite3.connect("noor_records.db")
                    c = conn.cursor()
                    c.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)", 
                              (u_name, u_email, u_msg))
                    conn.commit()
                    conn.close()
                    st.success("Message sent successfully! Noor will get back to you soon.")
                else:
                    st.error("Please fill in the required fields.")
    
    with info_col:
        st.markdown("#### Reach Out Directly")
        st.write("📧 info@abark.tech")
        st.write("📍 Islamabad, Pakistan")
        st.write("🔗 [LinkedIn](#)")