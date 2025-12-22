import streamlit as st
import pandas as pd
import sqlite3

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    # Table for Students
    c.execute('''CREATE TABLE IF NOT EXISTS students 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, grade_level TEXT, parent_contact TEXT)''')
    # Table for Grades
    c.execute('''CREATE TABLE IF NOT EXISTS grades 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  student_name TEXT, subject TEXT, score INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏫 EduManage POC")
st.sidebar.divider()
page = st.sidebar.radio("School Modules:", 
                       ["Dashboard", "Student Directory", "Gradebook", "Add New Entry"])

# --- MODULE 1: DASHBOARD ---
if page == "Dashboard":
    st.title("📈 School Overview")
    
    conn = sqlite3.connect("school.db")
    df_students = pd.read_sql_query("SELECT * FROM students", conn)
    df_grades = pd.read_sql_query("SELECT * FROM grades", conn)
    conn.close()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", len(df_students))
    
    if not df_grades.empty:
        avg_score = df_grades['score'].mean()
        col2.metric("Average GPA/Score", f"{avg_score:.1f}%")
        
        st.subheader("Performance by Subject")
        chart_data = df_grades.groupby('subject')['score'].mean()
        st.bar_chart(chart_data)
    else:
        st.info("Enroll students and add grades to see analytics.")

# --- MODULE 2: STUDENT DIRECTORY ---
elif page == "Student Directory":
    st.title("👥 Student Directory")
    conn = sqlite3.connect("school.db")
    df = pd.read_sql_query("SELECT * FROM students", conn)
    conn.close()
    
    search = st.text_input("Search Student Name")
    if search:
        df = df[df['name'].str.contains(search, case=False)]
    
    st.dataframe(df, use_container_width=True, hide_index=True)

# --- MODULE 3: GRADEBOOK ---
elif page == "Gradebook":
    st.title("📝 Student Gradebook")
    conn = sqlite3.connect("school.db")
    df = pd.read_sql_query("SELECT * FROM grades", conn)
    conn.close()
    
    if not df.empty:
        st.table(df) # Using st.table for a cleaner "report card" look
    else:
        st.warning("No grades recorded yet.")

# --- MODULE 4: ADD NEW ENTRY ---
elif page == "Add New Entry":
    st.title("➕ Administrative Entry")
    
    tab1, tab2 = st.tabs(["Enroll Student", "Record Grade"])
    
    with tab1:
        with st.form("enroll_form"):
            s_name = st.text_input("Student Name")
            s_grade = st.selectbox("Grade Level", [f"Grade {i}" for i in range(1, 13)])
            s_contact = st.text_input("Parent Contact (Phone/Email)")
            if st.form_submit_button("Enroll Student"):
                conn = sqlite3.connect("school.db")
                c = conn.cursor()
                c.execute("INSERT INTO students (name, grade_level, parent_contact) VALUES (?, ?, ?)", 
                          (s_name, s_grade, s_contact))
                conn.commit()
                conn.close()
                st.success(f"Registered {s_name}!")

    with tab2:
        # Get list of students for the dropdown
        conn = sqlite3.connect("school.db")
        student_list = pd.read_sql_query("SELECT name FROM students", conn)['name'].tolist()
        conn.close()

        with st.form("grade_form"):
            student = st.selectbox("Select Student", student_list) if student_list else st.info("Enroll students first!")
            subject = st.selectbox("Subject", ["Math", "Science", "English", "History", "Arts"])
            score = st.slider("Score", 0, 100, 75)
            if st.form_submit_button("Submit Grade"):
                conn = sqlite3.connect("school.db")
                c = conn.cursor()
                c.execute("INSERT INTO grades (student_name, subject, score) VALUES (?, ?, ?)", 
                          (student, subject, score))
                conn.commit()
                conn.close()
                st.balloons() # Fun visual effect
                st.success(f"Grade added for {student}!")