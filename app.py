import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, category TEXT, quantity INTEGER, price REAL)''')
    conn.commit()
    conn.close()

init_db()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("📦 IMS Portal")
st.sidebar.divider()
page = st.sidebar.radio("Navigate to:", ["Dashboard", "Inventory List", "Add/Update Stock"])

# --- PAGE 1: DASHBOARD ---
if page == "Dashboard":
    st.title("📊 Business Overview")
    
    conn = sqlite3.connect("inventory.db")
    df = pd.read_sql_query("SELECT * FROM items", conn)
    conn.close()

    if not df.empty:
        # High-level Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Items", len(df))
        col2.metric("Total Value", f"${(df['quantity'] * df['price']).sum():,.2f}")
        col3.metric("Low Stock Alerts", len(df[df['quantity'] < 5]))

        st.subheader("Inventory Distribution")
        st.bar_chart(df.set_index('name')['quantity'])
    else:
        st.info("No data available. Go to 'Add/Update Stock' to begin.")

# --- PAGE 2: INVENTORY LIST ---
elif page == "Inventory List":
    st.title("📋 Current Inventory")
    conn = sqlite3.connect("inventory.db")
    df = pd.read_sql_query("SELECT * FROM items", conn)
    conn.close()
    
    # Search Bar
    search = st.text_input("Search by Product Name")
    if search:
        df = df[df['name'].str.contains(search, case=False)]
    
    st.dataframe(df, use_container_width=True, hide_index=True)

# --- PAGE 3: ADD/UPDATE STOCK ---
elif page == "Add/Update Stock":
    st.title("➕ Stock Management")
    
    with st.form("add_form"):
        name = st.text_input("Product Name")
        cat = st.selectbox("Category", ["Electronics", "Furniture", "Food", "Apparel"])
        qty = st.number_input("Quantity", min_value=0, step=1)
        prc = st.number_input("Unit Price ($)", min_value=0.0, step=0.01)
        
        if st.form_submit_button("Save to Database"):
            if name:
                conn = sqlite3.connect("inventory.db")
                c = conn.cursor()
                c.execute("INSERT INTO items (name, category, quantity, price) VALUES (?, ?, ?, ?)", 
                          (name, cat, qty, prc))
                conn.commit()
                conn.close()
                st.success(f"Successfully added {name}!")
            else:
                st.error("Product Name is required.")