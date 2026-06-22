import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
import time

# --- 1. КОНФИГУРАЦИЯ И СТИЛИ ---
st.set_page_config(page_title="CLEAR REPORT", layout="wide")

st.markdown("""
    <style>
    /* Скрываем системный мусор, но ОСТАВЛЯЕМ стрелку сайдбара */
    .stDeployButton {display:none !important;}
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}

    /* Делаем верхнюю панель прозрачной, чтобы стрелочка меню (> / <) была видна и кликабельна */
    header {background-color: transparent !important;}

    /* Перекрашиваем главные кнопки (primary) в синий цвет */
    button[kind="primary"] {
        background-color: #007BFF !important;
        border-color: #007BFF !important;
        color: white !important;
    }
    button[kind="primary"]:hover {
        background-color: #0056b3 !important;
        border-color: #0056b3 !important;
    }

    /* Подкрашиваем стрелочку в выпадающих списках (selectbox) */
    div[data-testid="stSelectbox"] svg {
        fill: #007BFF !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    /* Стили для метрик и карточек */
    div[data-testid="stMetric"] {
        background-color: rgba(125, 125, 125, 0.05);
        border: 1px solid rgba(125, 125, 125, 0.1);
        padding: 15px;
        border-radius: 10px;
    }
    .help-card {
        padding: 15px;
        border-radius: 8px;
        background-color: rgba(0, 123, 255, 0.05);
        border-left: 5px solid #007BFF;
        margin-bottom: 10px;
    }

    /* Стилизация лендинга */
    .landing-header {
        text-align: center;
        margin-bottom: 1rem;
    }
    .landing-subheader {
        text-align: center;
        margin-bottom: 3rem;
        color: #6c757d;
        font-weight: normal;
    }
    .landing-text {
        font-size: 1.1rem;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. УПРАВЛЕНИЕ СОСТОЯНИЯМИ ---

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'show_login_form' not in st.session_state:
    st.session_state.show_login_form = False


def login_user(user, pwd):
    if user == "test" and pwd == "12345678":
        st.session_state.logged_in = True
        st.success("Доступ разрешен. Загрузка ядра...")
        time.sleep(0.5)
        st.rerun()
    else:
        st.error("Неверный логин или пароль")


def logout_user():
    st.session_state.logged_in = False
    st.session_state.show_login_form = False
    st.rerun()


def go_to_login():
    st.session_state.show_login_form = True
    st.rerun()


def go_back_to_landing():
    st.session_state.show_login_form = False
    st.rerun()


# --- 3. МАРШРУТИЗАЦИЯ ДО ВХОДА ---

if not st.session_state.logged_in:

    # 3.1. ЛЕНДИНГ (Вводная страница)
    if not st.session_state.show_login_form:
        st.markdown('<h1 class="landing-header">CLEAR REPORT</h1>', unsafe_allow_html=True)
        st.markdown('<h3 class="landing-subheader">Экосистема автоматизированного контроля рекламных размещений</h3>',
                    unsafe_allow_html=True)

        _, col2, _ = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div class="landing-text">
            <b>Система «CLEAR REPORT»</b> — это ваш надежный юридический и технический фильтр в сфере цифрового маркетинга. Мы помогаем бизнесу соблюдать требования ФЗ-347, автоматизируя процессы маркировки и передачи данных в ЕРИР.
            <br><br>
            <b>КЛЮЧЕВЫЕ ВОЗМОЖНОСТИ ПЛАТФОРМЫ:</b>
            <ul>
                <li><b>Интеллектуальная валидация:</b> Автоматическая проверка креативов на наличие обязательных маркеров («Реклама», токен erid). Снижение риска штрафов до 0%.</li>
                <li><b>Учет и систематизация:</b> Единый реестр контрагентов и рекламных кампаний для контроля всей цепочки размещений.</li>
                <li><b>Мониторинг активности:</b> Отслеживание статусов токенов, бюджетов и количества просмотров в режиме реального времени.</li>
                <li><b>Генерация отчетности:</b> Формирование готовых пакетов данных в формате Excel для операторов рекламных данных (ОРД) в один клик.</li>
            </ul>
            <i>Доверьте рутину алгоритмам. Сосредоточьтесь на эффективности.</i>
            </div>
            """, unsafe_allow_html=True)

            st.write("---")
            if st.button("ВОЙТИ В СИСТЕМУ", use_container_width=True, type="primary"):
                go_to_login()

    # 3.2. ФОРМА ВХОДА И РЕГИСТРАЦИИ
    else:
        st.button("Вернуться на главную", on_click=go_back_to_landing)

        _, center_col, _ = st.columns([1, 1, 1])

        with center_col:
            st.subheader("Авторизация")

            with st.form("login_form"):
                user = st.text_input("Логин", placeholder="test")
                pwd = st.text_input("Пароль", type="password", placeholder="••••••••")

                c1, c2 = st.columns(2)
                with c1:
                    submit = st.form_submit_button("ВОЙТИ", use_container_width=True)
                with c2:
                    register = st.form_submit_button("РЕГИСТРАЦИЯ", use_container_width=True)

                if submit:
                    login_user(user, pwd)
                if register:
                    st.info("Форма регистрации будет доступна после подключения базы данных.")

    st.stop()

# --- 4. ОСНОВНОЕ ПРИЛОЖЕНИЕ ---

with st.sidebar:
    st.title("CLEAR REPORT")
    st.caption("СИСТЕМА ИНТЕЛЛЕКТУАЛЬНОЙ МАРКИРОВКИ")
    st.write("---")

    menu = st.selectbox(
        "РАЗДЕЛ СИСТЕМЫ:",
        ["АНАЛИТИКА И МОНИТОРИНГ", "ВАЛИДАЦИЯ ТЕКСТА", "РЕЕСТР", "ФОРМИРОВАНИЕ И ЭКСПОРТ"]
    )
    st.write("---")
    if st.button("ВЫЙТИ ИЗ СИСТЕМЫ"):
        logout_user()

if menu == "АНАЛИТИКА И МОНИТОРИНГ":
    st.header("ПАНЕЛЬ УПРАВЛЕНИЯ")
    c1, c2, c3 = st.columns(3)
    c1.metric("АКТИВНЫЕ erid", "154", help="Токены в ротации")
    c2.metric("ВАЛИДНОСТЬ", "100%")
    c3.metric("ОБОРОТ", "840 000 ₽")

    st.write("---")

    col_graph, col_info = st.columns([2, 1])
    with col_graph:
        st.subheader("ДИНАМИКА МАРКИРОВКИ")
        fig = go.Figure(go.Scatter(x=['Нед 1', 'Нед 2', 'Нед 3', 'Нед 4'], y=[120, 180, 150, 210],
                                   line=dict(color='#007BFF', width=4), mode='lines+markers'))
        fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.subheader("ИНФОРМАЦИЯ")
        st.markdown("""
        <div class="help-card">
            <b>Система CLEAR REPORT</b> автоматически связывает ваши креативы с базой данных ЕРИР.
        </div>
        """, unsafe_allow_html=True)

elif menu == "ВАЛИДАЦИЯ ТЕКСТА":
    st.header("ПРОВЕРКА НА СООТВЕТСТВИЕ ФЗ-347")
    input_text = st.text_area("ТЕКСТ ОБЪЯВЛЕНИЯ", height=200)

    if st.button("ЗАПУСТИТЬ АНАЛИЗ"):
        if input_text:
            with st.status("CLEAR REPORT анализирует данные...") as s:
                time.sleep(1)
                has_erid = "erid" in input_text.lower()
                has_adv = "реклама" in input_text.lower()

                if has_erid and has_adv:
                    st.success("ТЕКСТ ПРОШЕЛ ПРОВЕРКУ: Все маркеры найдены.")
                else:
                    st.error("ОБНАРУЖЕНЫ ОШИБКИ:")
                    if not has_erid: st.warning("Отсутствует токен (erid)")
                    if not has_adv: st.warning("Отсутствует пометка 'Реклама'")

                s.update(label="Анализ завершен", state="complete")
        else:
            st.info("Пожалуйста, введите текст для проверки.")

elif menu == "РЕЕСТР":
    st.header("РЕЕСТР КОНТРАГЕНТОВ")
    df = pd.DataFrame({
        "КЛИЕНТ": ["ООО МЕДИАСЕТЬ", "ИП СМИРНОВ", "ООО КРЕАТИВ", "ООО АВРОРА"],
        "ИНН": ["7701445522", "500111223344", "7810556677", "7704556611"],
        "ТОКЕНОВ": [45, 12, 97, 3],
        "СТАТУС": ["ПРОВЕРЕН", "ПРОВЕРЕН", "ПРОВЕРЕН", "ПРОВЕРЕН"]
    })
    st.table(df)

elif menu == "ФОРМИРОВАНИЕ И ЭКСПОРТ":
    st.header("ФОРМИРОВАНИЕ И ЭКСПОРТ ОТЧЕТНОСТИ")
    period = st.selectbox("ПЕРИОД:", ["ЯНВАРЬ 2026", "ФЕВРАЛЬ 2026"])

    # ИЗМЕНЕНИЕ: Динамическое разделение данных по месяцам
    if period == "ЯНВАРЬ 2026":
        report_df = pd.DataFrame({
            "Дата": ["01.01.2026", "15.01.2026", "20.01.2026"],
            "erid": ["77vJ6fGvRb", "2VtzquZ1aX", "5UGfwMukZ4"],
            "Сумма (руб)": [150000, 45000, 120000],
            "Кол-во просмотров": [500000, 150000, 400000],
            "Стоимость одного просмотра": [0.30, 0.30, 0.30],
            "Статус": ["Подтвержден", "Подтвержден", "Ожидание акт"]
        })
    else:  # ФЕВРАЛЬ 2026
        report_df = pd.DataFrame({
            "Дата": ["04.02.2026", "14.02.2026", "28.02.2026"],
            "erid": ["99xK8hWvYn", "4MpqtrZ2bB", "8ZJfvNukX1"],
            "Сумма (руб)": [195000, 60000, 140000],
            "Кол-во просмотров": [650000, 200000, 430000],
            "Стоимость одного просмотра": [0.30, 0.30, 0.32],
            "Статус": ["Подтвержден", "Подтвержден", "Подтвержден"]
        })

    # Выводим интерактивную таблицу, которая теперь зависит от выбора
    st.table(report_df)
    st.write("---")

    # Компилируем Excel "на лету" из текущего report_df
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        report_df.to_excel(writer, index=False, sheet_name=f'Отчет_{period.replace(" ", "_")}')
    excel_data = output.getvalue()

    # Кнопка скачивания заберет именно те данные, которые сгенерировались в if-else выше
    st.download_button(
        label=f"СКАЧАТЬ ОТЧЕТ ЗА {period} (.XLSX)",
        data=excel_data,
        file_name=f"CLEAR REPORT_Report_{period.replace(' ', '_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        type="primary"
    )
