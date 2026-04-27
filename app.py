import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# 1. Системная настройка страницы
st.set_page_config(
    page_title="AD-MARK CORE",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Адаптивный дизайн (работает для светлой и темной темы)
st.markdown("""
    <style>
    /* Общие отступы и шрифты */
    .main { font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }

    /* Стилизация карточек метрик */
    div[data-testid="stMetric"] {
        background-color: rgba(125, 125, 125, 0.1);
        border: 1px solid rgba(125, 125, 125, 0.2);
        padding: 15px 20px;
        border-radius: 10px;
    }

    /* Стилизация пояснительных блоков */
    .help-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: rgba(0, 123, 255, 0.05);
        border-left: 4px solid #007BFF;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }

    /* Фикс кнопок */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        font-weight: 500;
    }

    /* Заголовки с иконками */
    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ЛЕВАЯ ПАНЕЛЬ (НАВИГАЦИЯ) ---
with st.sidebar:
    st.title("AD-MARK // CORE")
    st.write("---")

    choice = st.selectbox(
        "РАЗДЕЛ СИСТЕМЫ",
        ["МОНИТОРИНГ", "ВАЛИДАЦИЯ", "РЕЕСТР", "ОТЧЕТНОСТЬ"],
        help="Выберите модуль для работы с данными маркировки"
    )

    st.write("---")
    st.caption("Версия системы: 1.1.0")
    st.caption("Статус соединения с ЕРИР: Активен")

# --- ЛОГИКА МОДУЛЕЙ ---

if choice == "МОНИТОРИНГ":
    st.subheader("МОНИТОРИНГ ПОКАЗАТЕЛЕЙ")

    # Метрики с пояснениями через help
    col1, col2, col3 = st.columns(3)
    col1.metric("АКТИВНЫЕ ТОКЕНЫ", "154",
                help="Количество идентификаторов (erid), находящихся в ротации в текущем месяце")
    col2.metric("ВАЛИДАЦИЯ", "100%", help="Процент данных, прошедших автоматическую проверку на соответствие ФЗ-347")
    col3.metric("ОБОРОТ (МЕСЯЦ)", "840 000 ₽",
                help="Суммарный объем финансовых обязательств по зарегистрированным договорам")

    st.write("---")

    c_left, c_right = st.columns([2, 1])

    with c_left:
        st.markdown('<div class="section-header"><h4>ГРАФИК АКТИВНОСТИ РАЗМЕЩЕНИЙ</h4></div>', unsafe_allow_html=True)
        # График, который подстраивается под тему
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=['Нед 1', 'Нед 2', 'Нед 3', 'Нед 4'],
            y=[120, 180, 150, 210],
            mode='lines+markers',
            line=dict(color='#007BFF', width=3)
        ))
        fig.update_layout(
            template="none",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=0),
            height=300,
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor='rgba(125,125,125,0.2)')
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with c_right:
        st.markdown('<div class="section-header"><h4>СТАТУС ЕРИР</h4></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="help-box">
            <b>Последний токен:</b><br>
            <code>77vJ6fGvR</code><br>
            Статус: Подтвержден
        </div>
        <div class="help-box">
            <b>Очередь обработки:</b><br>
            Объектов: 12<br>
            Ожидание: 0.4 сек
        </div>
        """, unsafe_allow_html=True)

elif choice == "ВАЛИДАЦИЯ":
    st.subheader("ИНТЕЛЛЕКТУАЛЬНАЯ ПРОВЕРКА")
    st.write("Проверка рекламных материалов на соответствие требованиям ст. 18.1 ФЗ 'О рекламе'.")

    input_text = st.text_area("ТЕКСТ ДЛЯ АНАЛИЗА", height=200,
                              help="Вставьте текст рекламного объявления, включая информацию о рекламодателе и erid")

    if st.button("ЗАПУСТИТЬ ПРОВЕРКУ"):
        with st.status("Выполняется лингвистический анализ...") as status:
            time.sleep(1)
            has_erid = "erid" in input_text.lower()
            has_adv = "реклама" in input_text.lower()
            status.update(label="Проверка завершена", state="complete")

        if has_erid and has_adv:
            st.success("Нарушений не выявлено. Все обязательные атрибуты присутствуют.")
        else:
            st.error("Обнаружены несоответствия:")
            if not has_erid: st.info("Отсутствует буквенно-цифровой код erid (токен).")
            if not has_adv: st.info("Отсутствует обязательная пометка 'Реклама'.")

elif choice == "РЕЕСТР":
    st.subheader("РЕЕСТР КОНТРАГЕНТОВ И ДОГОВОРОВ")
    st.write("Централизованная база данных участников рекламной цепочки.")

    df = pd.DataFrame({
        "ID": ["102", "105", "110"],
        "КОНТРАГЕНТ": ["ООО МЕДИАСЕТЬ", "ИП СМИРНОВ", "ООО КРЕАТИВ"],
        "ИНН": ["7701445522", "500111223344", "7810556677"],
        "ТОКЕНОВ": [45, 12, 97],
        "СТАТУС": ["ПРОВЕРЕН", "ПРОВЕРЕН", "ПРОВЕРЕН"]
    })

    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption("Данные синхронизированы с ЕГРЮЛ/ЕГРИП")

elif choice == "ОТЧЕТНОСТЬ":
    st.subheader("ФОРМИРОВАНИЕ ОТЧЕТНОСТИ")
    st.write("Подготовка данных для передачи Операторам Рекламных Данных (ОРД).")

    period = st.selectbox("ОТЧЕТНЫЙ ПЕРИОД", ["Январь 2026", "Февраль 2026"])

    st.markdown('<div class="section-header"><b>ГОТОВНОСТЬ ДАННЫХ</b></div>', unsafe_allow_html=True)
    st.progress(0.85, text="85% объектов валидировано")

    if st.button("СФОРМИРОВАТЬ ПАКЕТ ДАННЫХ"):
        st.toast("Файл подготовлен")
        st.download_button("СКАЧАТЬ (.XML)", data="DATA", file_name=f"report_{period}.xml")
