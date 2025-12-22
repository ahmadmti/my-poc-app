import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("pizza_admin.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  customer TEXT, pizza_type TEXT, size TEXT, 
                  status TEXT, price REAL, timestamp DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# --- FANCY UI/UX CUSTOMIZATION ---
st.set_page_config(page_title="SliceMaster Pro", page_icon="🍕", layout="wide")

# Custom CSS for a "Brand" look
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; color: white; }
    .stButton>button { background-color: #ff4b4b; color: white; border-radius: 20px; border: none; }
    .stMetric { background-color: #262730; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAV ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3595/3595455.png", width=100)
st.sidebar.title("SliceMaster Admin")
page = st.sidebar.selectbox("Go to:", ["🔥 Live Orders", "🍕 Create New Order", "📊 Sales Insights"])

# --- PAGE 1: LIVE ORDERS ---
if page == "🔥 Live Orders":
    st.title("🔥 Current Kitchen Queue")
    conn = sqlite3.connect("pizza_admin.db")
    df = pd.read_sql_query("SELECT * FROM orders WHERE status != 'Delivered' ORDER BY timestamp DESC", conn)
    conn.close()

    if not df.empty:
        # Using columns to create "Order Cards"
        for index, row in df.iterrows():
            with st.container():
                c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
                c1.subheader(f"#{row['id']}")
                c2.markdown(f"**{row['customer']}** - {row['size']} {row['pizza_type']}")
                c3.warning(f"Status: {row['status']}")
                if c4.button("Mark Delivered", key=f"btn_{row['id']}"):
                    conn = sqlite3.connect("pizza_admin.db")
                    c = conn.cursor()
                    c.execute("UPDATE orders SET status = 'Delivered' WHERE id = ?", (row['id'],))
                    conn.commit()
                    conn.close()
                    st.rerun()
                st.divider()
    else:
        st.success("Kitchen is clear! No pending orders.")

# --- PAGE 2: CREATE NEW ORDER ---
elif page == "🍕 Create New Order":
    st.title("🍕 Take an Order")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Customer Details")
        cust_name = st.text_input("Customer Name")
        pizza = st.selectbox("Select Pizza", ["Margherita", "Pepperoni", "BBQ Chicken", "Veggie Supreme", "Hawaiian"])
        size = st.select_slider("Size", options=["Personal", "Medium", "Large", "Family"])
    
    with col2:
        st.subheader("Pricing & Confirmation")
        prices = {"Personal": 8.0, "Medium": 12.0, "Large": 16.0, "Family": 20.0}
        current_price = prices[size]
        st.metric("Total Price", f"${current_price:.2f}")
        
        if st.button("Confirm & Send to Kitchen"):
            if cust_name:
                conn = sqlite3.connect("pizza_admin.db")
                c = conn.cursor()
                c.execute("INSERT INTO orders (customer, pizza_type, size, status, price, timestamp) VALUES (?, ?, ?, ?, ?, ?)", 
                          (cust_name, pizza, size, 'Cooking', current_price, datetime.now()))
                conn.commit()
                conn.close()
                st.balloons()
                st.toast(f"Order for {cust_name} sent to kitchen!", icon="🍕")
            else:
                st.error("Please enter a customer name.")

# --- PAGE 3: SALES INSIGHTS ---
elif page == "📊 Sales Insights":
    st.title("📊 Restaurant Performance")
    conn = sqlite3.connect("pizza_admin.db")
    df = pd.read_sql_query("SELECT * FROM orders", conn)
    conn.close()

    if not df.empty:
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Revenue", f"${df['price'].sum():,.2f}")
        m2.metric("Total Pizzas Sold", len(df))
        m3.metric("Avg Order Value", f"${df['price'].mean():.2f}")

        st.subheader("Popular Pizzas")
        pizza_counts = df['pizza_type'].value_counts()
        st.bar_chart(pizza_counts)
    else:
        st.info("No sales data recorded yet.")