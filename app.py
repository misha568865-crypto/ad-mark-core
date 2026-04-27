import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# Принудительная настройка страницы
st.set_page_config(
    page_title="АД-МАРК CORE",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ЖЕСТКИЙ CSS: БЛОКИРОВКА СВЕТЛОЙ ТЕМЫ И ЧИСТКА ИНТЕРФЕЙСА ---
st.markdown("""
    <style>
    /* 1. Блокируем фон приложения и убираем верхнюю полосу */
    header, .stApp {
        background-color: #0E1117 !important;
    }

    /* 2. Скрываем кнопку смены темы и лишние меню */
    #MainMenu, header, footer {
        visibility: hidden !important;
        height: 0 !important;
    }

    /* 3. Делаем кнопку развертывания сайдбара видимой (фикс прошлой ошибки) */
    button[data-testid="sidebar-button"] {
        visibility: visible !important;
        background-color: #1C2028 !important;
        color: white !important;
        position: fixed !important;
        top: 10px !important;
        left: 10px !important;
        z-index: 999999 !important;
    }

    /* 4. Принудительный темный цвет для всех элементов */
    section[data-testid="stSidebar"] {
        background-color: #0B0E14 !important;
        border-right: 1px solid #2D333B !important;
    }

    div[data-testid="stMetric"] {
        background: #1C2028 !important;
        border: 1px solid #2D333B !important;
        border-radius: 8px !important;
    }

    /* 5. Фикс текста: всегда белый */
    h1, h2, h3, h4, p, span, label, .stMarkdown {
        color: #FFFFFF !important;
    }

    .stSelectbox div[data-baseweb="select"] {
        background-color: #1C2028 !important;
        color: white !important;
    }

    /* Кнопки */
    div.stButton > button {
        background-color: #007BFF !important;
        color: white !important;
        border: none !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- НАВИГАЦИЯ ---
with st.sidebar:
    st.markdown("### АД-МАРК // CORE")
    st.write("---")

    choice = st.selectbox(
        "РАЗДЕЛ СИСТЕМЫ:",
        ["МОНИТОРИНГ", "ПРОВЕРКА", "РЕЕСТР", "ОТЧЕТНОСТЬ"]
    )
    # Плашка "Статус ок" удалена по твоей просьбе

# --- КОНТЕНТ ---

if choice == "МОНИТОРИНГ":
    st.markdown("## МОНИТОРИНГ ПОКАЗАТЕЛЕЙ")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("ТОКЕНЫ (erid)", "154", help="Уникальный номер каждой рекламы")
    with c2:
        st.metric("ВАЛИДАЦИЯ (проверка)", "100%", help="Процент верных данных")
    with c3:
        st.metric("ОБОРОТ (МЕСЯЦ)", "840 000 ₽")

    st.write("---")
    st.subheader("ГРАФИК АКТИВНОСТИ")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=['Нед 1', 'Нед 2', 'Нед 3', 'Нед 4'],
        y=[120, 180, 150, 210],
        mode='lines+markers',
        line=dict(color='#007BFF', width=3),
        marker=dict(size=8, color='#FFFFFF')
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#FFFFFF",
        height=350,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=False, fixedrange=True),
        yaxis=dict(showgrid=True, gridcolor='#2D333B', fixedrange=True),
        hovermode=False
    )

    st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})

elif choice == "ПРОВЕРКА":
    st.markdown("## ИИ-АНАЛИЗ МАРКИРОВКИ")
    input_text = st.text_area("ТЕКСТ ОБЪЯВЛЕНИЯ:", height=200)

    if st.button("ЗАПУСТИТЬ АНАЛИЗ"):
        with st.status("Сканирование...") as s:
            time.sleep(0.6)
            has_erid = "erid" in input_text.lower()
            has_adv = "реклама" in input_text.lower()
            s.update(label="Готово", state="complete")

        if has_erid and has_adv:
            st.success("Маркировка корректна")
        else:
            st.error("Обнаружены ошибки")
            if not has_erid: st.info("Нет номера erid")
            if not has_adv: st.info("Нет пометки 'Реклама'")

elif choice == "РЕЕСТР":
    st.markdown("## РЕЕСТР КОНТРАГЕНТОВ")
    df = pd.DataFrame({
        "ID": ["102", "105", "110"],
        "КЛИЕНТ": ["ООО МЕДИАСЕТЬ", "ИП СМИРНОВ", "ООО КРЕАТИВ"],
        "ИНН": ["7701445522", "500111223344", "7810556677"],
        "СТАТУС": ["ПРОВЕРЕН", "ПРОВЕРЕН", "ПРОВЕРЕН"]
    })
    st.table(df)

elif choice == "ОТЧЕТНОСТЬ":
    st.markdown("## ЭКСПОРТ В ЕРИР")
    st.selectbox("ПЕРИОД:", ["ЯНВАРЬ 2026", "ФЕВРАЛЬ 2026"])
    if st.button("СФОРМИРОВАТЬ ОТЧЕТ"):
        st.download_button("СКАЧАТЬ XML", data="DATA", file_name="report.xml")