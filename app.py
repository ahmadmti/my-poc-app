import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("salon_bookings.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bookings 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  client_name TEXT, service TEXT, date TEXT, time TEXT, status TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- UI/UX CONFIG ---
st.set_page_config(page_title="Luxe Glow Studio", page_icon="✨", layout="wide")

# Custom CSS for a soft, elegant "Salon" feel
st.markdown("""
    <style>
    .stApp { background-color: #fffaf0; }
    h1, h2, h3 { color: #5d4037; font-family: 'Serif'; }
    .stButton>button { background-color: #d4a373; color: white; border-radius: 5px; width: 100%; border: none; }
    .service-card { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAV ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
st.sidebar.title("Luxe Glow Admin")
page = st.sidebar.radio("Navigation", ["✨ Welcome Home", "💅 Our Services", "📅 Book Appointment", "🔐 Staff Dashboard"])

# --- PAGE 1: LANDING PAGE (HERO) ---
if page == "✨ Welcome Home":
    st.title("Welcome to Luxe Glow Studio")
    st.markdown("#### *Where Beauty Meets Science and Soul*")
    
    # Hero Image
    st.image("https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&q=80&w=1200", use_container_width=True)
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("### Expert Stylists")
        st.write("Our team has over 15 years of experience in high-end fashion and bridal hair.")
    with col2:
        st.write("### Organic Products")
        st.write("We use 100% sulfate-free and paraben-free products for your hair and skin.")
    with col3:
        st.write("### Relaxing Atmosphere")
        st.write("Enjoy a complimentary glass of champagne and aromatherapy with every service.")

# --- PAGE 2: SERVICES ---
elif page == "💅 Our Services":
    st.title("Our Signature Services")
    
    c1, c2, c3 = st.columns(3)
    
    services = [
        {"name": "Hair Cut & Style", "price": "$85+", "img": "https://cdn-icons-png.flaticon.com/512/2932/2932159.png"},
        {"name": "Balayage Color", "price": "$180+", "img": "https://cdn-icons-png.flaticon.com/512/3059/3059434.png"},
        {"name": "HydraFacial", "price": "$120+", "img": "https://cdn-icons-png.flaticon.com/512/3209/3209144.png"}
    ]
    
    cols = [c1, c2, c3]
    for i, s in enumerate(services):
        with cols[i]:
            st.image(s['img'], width=80)
            st.subheader(s['name'])
            st.write(f"Starting at {s['price']}")
            if st.button(f"Book {s['name']}", key=i):
                st.info("Head to the Booking page to secure your slot!")

# --- PAGE 3: BOOKING ---
elif page == "📅 Book Appointment":
    st.title("Secure Your Glow")
    
    with st.form("booking_form"):
        name = st.text_input("Full Name")
        service = st.selectbox("Select Service", ["Hair Cut", "Full Color", "Facial", "Manicure/Pedicure", "Bridal Makeup"])
        b_date = st.date_input("Preferred Date")
        b_time = st.select_slider("Preferred Time", options=["09:00 AM", "11:00 AM", "01:00 PM", "03:00 PM", "05:00 PM"])
        
        if st.form_submit_button("Request Appointment"):
            if name:
                conn = sqlite3.connect("salon_bookings.db")
                c = conn.cursor()
                c.execute("INSERT INTO bookings (client_name, service, date, time, status) VALUES (?, ?, ?, ?, ?)", 
                          (name, service, str(b_date), b_time, "Pending"))
                conn.commit()
                conn.close()
                st.success(f"Thank you {name}! We will confirm your appointment for {b_date} at {b_time} shortly.")
                st.balloons()
            else:
                st.error("Please enter your name.")

# --- PAGE 4: STAFF DASHBOARD ---
elif page == "🔐 Staff Dashboard":
    st.title("Admin Appointments")
    
    conn = sqlite3.connect("salon_bookings.db")
    df = pd.read_sql_query("SELECT * FROM bookings", conn)
    conn.close()
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.download_button("Download Schedule as CSV", df.to_csv(index=False), "salon_schedule.csv")
    else:
        st.info("No bookings yet.")