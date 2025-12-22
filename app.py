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

# --- FANCY UI/UX ---
st.set_page_config(page_title="SliceMaster Pro + AI", page_icon="🍕", layout="wide")

st.markdown("""
    <style>
    .stChatFloatingInputContainer { background-color: #1a1a1a; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAV ---
st.sidebar.title("🍕 SliceMaster AI")
page = st.sidebar.selectbox("Go to:", ["🤖 AI Assistant", "🔥 Live Orders", "🍕 Create New Order", "📊 Sales Insights"])

# --- MODULE: AI CHATBOT assistant ---
if page == "🤖 AI Assistant":
    st.title("🤖 Pizza Assistant")
    st.info("Ask me about our menu, prices, or how to place an order!")

    # Initialize chat history (This is like $_SESSION in PHP)
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Ciao! I'm the SliceMaster AI. How can I help you today?"}]

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Type your question here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # GENERATE BOT RESPONSE (Rule-based for POC)
        response = ""
        p = prompt.lower()
        
        if "menu" in p or "pizzas" in p:
            response = "We have: Margherita, Pepperoni, BBQ Chicken, Veggie Supreme, and Hawaiian!"
        elif "price" in p or "cost" in p:
            response = "Our prices range from $8.00 for a Personal to $20.00 for a Family size."
        elif "order" in p:
            response = "You can place an order by clicking 'Create New Order' in the sidebar!"
        elif "hello" in p or "hi" in p:
            response = "Hello! Ready for the best pizza in town?"
        else:
            response = "I'm still learning! You can ask me about our 'menu', 'prices', or how to 'order'."

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- PAGE 1: LIVE ORDERS ---
elif page == "🔥 Live Orders":
    st.title("🔥 Current Kitchen Queue")
    conn = sqlite3.connect("pizza_admin.db")
    df = pd.read_sql_query("SELECT * FROM orders WHERE status != 'Delivered' ORDER BY timestamp DESC", conn)
    conn.close()

    if not df.empty:
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
        st.success("Kitchen is clear!")

# --- PAGE 2: CREATE NEW ORDER ---
elif page == "🍕 Create New Order":
    st.title("🍕 Take an Order")
    col1, col2 = st.columns(2)
    with col1:
        cust_name = st.text_input("Customer Name")
        pizza = st.selectbox("Select Pizza", ["Margherita", "Pepperoni", "BBQ Chicken", "Veggie Supreme", "Hawaiian"])
        size = st.select_slider("Size", options=["Personal", "Medium", "Large", "Family"])
    with col2:
        prices = {"Personal": 8.0, "Medium": 12.0, "Large": 16.0, "Family": 20.0}
        current_price = prices[size]
        st.metric("Total Price", f"${current_price:.2f}")
        if st.button("Confirm Order"):
            if cust_name:
                conn = sqlite3.connect("pizza_admin.db")
                c = conn.cursor()
                c.execute("INSERT INTO orders (customer, pizza_type, size, status, price, timestamp) VALUES (?, ?, ?, ?, ?, ?)", 
                          (cust_name, pizza, size, 'Cooking', current_price, datetime.now()))
                conn.commit()
                conn.close()
                st.balloons()
            else:
                st.error("Enter customer name.")

# --- PAGE 3: SALES INSIGHTS ---
elif page == "📊 Sales Insights":
    st.title("📊 Performance")
    conn = sqlite3.connect("pizza_admin.db")
    df = pd.read_sql_query("SELECT * FROM orders", conn)
    conn.close()
    if not df.empty:
        m1, m2 = st.columns(2)
        m1.metric("Total Revenue", f"${df['price'].sum():,.2f}")
        m2.metric("Orders", len(df))
        st.bar_chart(df['pizza_type'].value_counts())