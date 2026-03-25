import streamlit as st
import pandas as pd
from datetime import date

# Настройка страницы
st.set_page_config(page_title="Чунджа Межгород :: CyberLink", page_icon="⚡", layout="wide")

# --- СТИЛЬ КИБЕРПАНК ---
cyberpunk_css = """
<style>
    .stApp {
        background-image: 
            linear-gradient(rgba(13, 1, 24, 0.8), rgba(13, 1, 24, 0.9)), 
            url("https://r.jina.ai/img/a_futuristic_cyberpunk_style_taxi_car_driving_through_a_neon_lit_rain_slicked_city_street_with_glowing_cyan_and_magenta_accents_and_visible_Chundja_text_on_the_side_954939b752.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #00ffff;
        font-family: 'Courier New', Courier, monospace;
    }
    h1, h2, h3 { color: #ff00ff !important; text-shadow: 0 0 10px #ff00ff; text-transform: uppercase; }
    .stTabs [data-baseweb="tab-list"] { background-color: rgba(26, 2, 41, 0.7); }
    .stTabs [data-baseweb="tab"] { color: #ff00ff; border: 1px solid #ff00ff; margin: 5px; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #ff00ff !important; color: #0d0118 !important; }
    .stSelectbox, .stTextInput, .stTextArea, .stDateInput > div > div > input {
        background-color: rgba(26, 2, 41, 0.8) !important;
        color: #00ffff !important;
        border: 1px solid #00ffff !important;
    }
    .stButton > button {
        background-color: transparent; color: #00ffff; border: 2px solid #00ffff;
        width: 100%; text-transform: uppercase; font-weight: bold; transition: 0.3s;
    }
    .stButton > button:hover { background-color: #00ffff; color: #0d0118; box-shadow: 0 0 20px #00ffff; }
    .streamlit-expanderHeader { background-color: rgba(26, 2, 41, 0.8) !important; border: 1px solid #ff00ff !important; color: #ff00ff !important; }
</style>
"""
st.markdown(cyberpunk_css, unsafe_allow_html=True)

if 'driver_trips' not in st.session_state: st.session_state.driver_trips = []
if 'passenger_requests' not in st.session_state: st.session_state.passenger_requests = []

st.title("🤖 ЧУНДЖА МЕЖГОРОД")
st.subheader("Сетевой протокол v1.5")

locations = ["Чунджа", "Алматы", "Жаркент", "Кольжат", "Горячие источники Чунджа", "Уйгурский р-н Чарын", "Уйгурский р-н Аксу"]

tab1, tab2 = st.tabs(["[ СЕКТОР ВОДИТЕЛЯ ]", "[ СЕКТОР ПАССАЖИРА ]"])

with tab1:
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.header("⚡ Регистрация машины")
        with st.form("driver_form"):
            dep = st.selectbox("Откуда", locations, key="d_from")
            dest = st.selectbox("Куда", locations, key="d_to")
            d_date = st.date_input("Дата выезда", min_value=date.today())
            tm = st.text_input("Время (ЧЧ:ММ)")
            ph = st.text_input("Ваш контакт")
            comment = st.text_area("Комментарий")
            if st.form_submit_button("ОПУБЛИКОВАТЬ РЕЙС"):
                if dep != dest and ph:
                    st.session_state.driver_trips.append({"откуда": dep, "куда": dest, "дата": d_date, "время": tm, "контакт": ph, "коммент": comment})
                    st.success("ПРОТОКОЛ ПРИНЯТ")
    with col2:
        st.header("🔍 Пассажиры ждут")
        search_p = st.selectbox("Направление:", locations, key="p_search")
        for p in [x for x in st.session_state.passenger_requests if x["куда"] == search_p]:
            with st.expander(f"👤 {p['откуда']} -> {p['куда']} | {p['дата']}"):
                st.write(f"📞 {p['контакт']}\n💬 {p['коммент']}")

with tab2:
    col3, col4 = st.columns([1, 1.5])
    with col3:
        st.header("⚡ Анкета пассажира")
        with st.form("passenger_form"):
            p_dep = st.selectbox("Откуда", locations, key="p_from")
            p_dest = st.selectbox("Куда", locations, key="p_to")
            p_date = st.date_input("Дата", min_value=date.today(), key="p_date_in")
            p_tm = st.text_input("Время")
            p_ph = st.text_input("Контакт")
            p_comment = st.text_area("Детали")
            if st.form_submit_button("РАЗМЕСТИТЬ ЗАЯВКУ"):
                if p_dep != p_dest and p_ph:
                    st.session_state.passenger_requests.append({"откуда": p_dep, "куда": p_dest, "дата": p_date, "время": p_tm, "контакт": p_ph, "коммент": p_comment})
                    st.success("ЗАЯВКА В СЕТИ")
    with col4:
        st.header("🚗 Доступные машины")
        search_d = st.selectbox("Куда едем?", locations, key="d_search")
        for d in [x for x in st.session_state.driver_trips if x["куда"] == search_d]:
            with st.expander(f"🏎️ {d['откуда']} -> {d['куда']} | {d['дата']}"):
                st.write(f"📞 {d['контакт']}\n💬 {d['коммент']}")
