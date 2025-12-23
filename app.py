import streamlit as st
import pandas as pd

# --- صفحہ کی ترتیبات ---
st.set_page_config(page_title="نور العین | آفیشل", page_icon="🌹", layout="wide")

# --- اردو فونٹ اور ڈیزائن کے لیے CSS ---
st.markdown("""
    <style>
    /* دائیں سے بائیں (RTL) زبان کی ترتیب */
    .main { text-align: right; direction: rtl; font-family: 'Noto Naskh Arabic', serif; }
    div[data-testid="stSidebarNav"] { direction: rtl; }
    
    /* ہیرو سیکشن کا اسٹائل */
    .hero { background-color: #1e1e1e; padding: 60px; border-radius: 15px; color: white; text-align: center; }
    
    /* سروسز کارڈز */
    .service-card { 
        background-color: #ffffff; padding: 20px; border-radius: 10px; 
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1); color: #333; text-align: center;
        margin-bottom: 20px;
    }
    
    /* فوٹر */
    .footer { background-color: #000; color: #aaa; padding: 20px; text-align: center; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- ٹاپ نیویگیشن (بذریعہ ریڈیو بٹن) ---
st.markdown("<h1 style='text-align: center;'>نور العین</h1>", unsafe_allow_html=True)
nav = st.radio("", ["ہوم", "ہماری خدمات", "تاثرات", "رابطہ کریں"], horizontal=True)

st.divider()

# --- 1. ہیرو سیکشن (Hero Section) ---
if nav == "ہوم":
    st.markdown("""
        <div class='hero'>
            <h1>خوش آمدید! میں ہوں نور العین</h1>
            <p style='font-size: 1.2rem;'>تعلیم، ٹیکنالوجی اور بہتر مستقبل کی جانب ایک قدم</p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&q=80&w=800")
    with col2:
        st.write("### میرے بارے میں")
        st.write("""
        میرا مقصد جدید علوم کے ذریعے معاشرے میں مثبت تبدیلی لانا ہے۔ 
        میں تخلیقی سوچ اور ٹیکنالوجی کے ملاپ پر یقین رکھتی ہوں۔ 
        اس ویب سائٹ کا مقصد اپنے کام اور خیالات کو دنیا کے سامنے پیش کرنا ہے۔
        """)
        st.button("مزید جانیں")

# --- 2. سروسز سیکشن (Services Section) ---
elif nav == "ہماری خدمات":
    st.markdown("<h2 style='text-align: center;'>ہماری خدمات</h2>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='service-card'><h3>تعلیمی رہنمائی</h3><p>طالب علموں کے لیے بہترین تعلیمی مشورے اور رہنمائی۔</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='service-card'><h3>ڈیجیٹل ڈیزائن</h3><p>خوبصورت اور جدید ویب ڈیزائننگ کی سہولیات۔</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='service-card'><h3>تخلیقی تحریر</h3><p>اردو اور انگریزی میں معیاری مواد کی تیاری۔</p></div>", unsafe_allow_html=True)

# --- 3. ٹیسٹیمونیلز (Testimonials) ---
elif nav == "تاثرات":
    st.markdown("<h2 style='text-align: center;'>لوگ ہمارے بارے میں کیا کہتے ہیں</h2>", unsafe_allow_html=True)
    
    t1, t2 = st.columns(2)
    with t1:
        st.info("نور العین کی کام کے ساتھ لگن اور ان کی تخلیقی صلاحیتیں واقعی متاثر کن ہیں۔ - **احمد علی**")
    with t2:
        st.success("بہترین کام اور وقت کی پابندی، ان کے ساتھ کام کرنا ایک اچھا تجربہ رہا۔ - **سارہ خان**")

# --- 4. رابطہ کریں (Contact) ---
elif nav == "رابطہ کریں":
    st.markdown("<h2 style='text-align: center;'>رابطہ کریں</h2>", unsafe_allow_html=True)
    with st.form("contact_urdu"):
        name = st.text_input("آپ کا نام")
        email = st.text_input("ای میل")
        msg = st.text_area("آپ کا پیغام")
        if st.form_submit_button("پیغام بھیجیں"):
            st.balloons()
            st.success("شکریہ! آپ کا پیغام ہمیں موصول ہو گیا ہے۔")

# --- فوٹر (Footer) ---
st.markdown("""
    <div class='footer'>
        <p>© 2025 نور العین | جملہ حقوق محفوظ ہیں</p>
        <p>ڈیزائن بذریعہ: ابارک ٹیک اسٹائل</p>
    </div>
    """, unsafe_allow_html=True)