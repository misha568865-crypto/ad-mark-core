import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
import time

# Настройка страницы
st.set_page_config(
    page_title="АПОЛОГЕТ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Стили для профессионального вида
st.markdown("""
    <style>
    .main { font-family: 'Segoe UI', sans-serif; }
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
    </style>
    """, unsafe_allow_html=True)

# --- САЙДБАР ---
with st.sidebar:
    st.title("Апологет")
    st.caption("СИСТЕМА ИНТЕЛЛЕКТУАЛЬНОЙ МАРКИРОВКИ")
    st.write("---")

    menu = st.selectbox(
        "РАЗДЕЛ СИСТЕМЫ:",
        ["МОНИТОРИНГ", "ВАЛИДАЦИЯ ТЕКСТА", "РЕЕСТР", "ГЕНЕРАЦИЯ ОТЧЕТА"]
    )
    st.write("---")
    st.info("База данных: Подключена")

# --- МОДУЛИ ---

if menu == "МОНИТОРИНГ":
    st.header("ПАНЕЛЬ УПРАВЛЕНИЯ")

    c1, c2, c3 = st.columns(3)
    c1.metric("АКТИВНЫЕ erid", "154", help="Токены в ротации за текущий период")
    c2.metric("ВАЛИДНОСТЬ", "100%", help="Проверка на соответствие ФЗ-347")
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
            <b>Система Апологет</b> автоматически связывает ваши креативы с базой данных ЕРИР.
        </div>
        <div class="help-card">
            Все токены проходят предварительную проверку перед публикацией.
        </div>
        """, unsafe_allow_html=True)

elif menu == "ВАЛИДАЦИЯ ТЕКСТА":
    st.header("ПРОВЕРКА НА СООТВЕТСТВИЕ ФЗ-347")
    st.write("Вставьте текст рекламного объявления для анализа ИИ-алгоритмом.")

    input_text = st.text_area("ТЕКСТ ОБЪЯВЛЕНИЯ", height=200, placeholder="Введите текст здесь...")

    if st.button("ЗАПУСТИТЬ АНАЛИЗ"):
        if input_text:
            # ФИКС: Всё, что внутри with st.status, теперь будет ВНУТРИ плашки
            with st.status("Апологет анализирует данные...") as s:
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
        "ID": ["102", "105", "110", "121"],
        "КЛИЕНТ": ["ООО МЕДИАСЕТЬ", "ИП СМИРНОВ", "ООО КРЕАТИВ", "ООО АВРОРА"],
        "ИНН": ["7701445522", "500111223344", "7810556677", "7704556611"],
        "ТОКЕНОВ": [45, 12, 97, 3],
        "СТАТУС": ["ПРОВЕРЕН", "ПРОВЕРЕН", "ПРОВЕРЕН", "ПРОВЕРЕН"]
    })
    st.dataframe(df, use_container_width=True, hide_index=True)

elif menu == "ГЕНЕРАЦИЯ ОТЧЕТА":
    st.header("ЭКСПОРТ ОТЧЕТНОСТИ")
    st.write("Сформируйте финальный файл для передачи в ОРД в формате Excel.")

    period = st.selectbox("ПЕРИОД:", ["ЯНВАРЬ 2026", "ФЕВРАЛЬ 2026"])

    report_df = pd.DataFrame({
        "Дата": ["01.01.2026", "15.01.2026", "20.01.2026"],
        "ID Кампании": ["CAM-001", "CAM-002", "CAM-003"],
        "erid": ["77vJ6fGvR", "2VtzquZ1a", "5BtzquX9b"],
        "Сумма (руб)": [150000, 45000, 120000],
        "Статус": ["Подтвержден", "Подтвержден", "Ожидание акт"]
    })

    st.write("Предпросмотр данных отчета:")
    st.table(report_df)

    if st.button("СФОРМИРОВАТЬ EXCEL"):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            report_df.to_excel(writer, index=False, sheet_name='Отчет_Апологет')

        excel_data = output.getvalue()

        st.success("Отчет «Апологет» сформирован!")
        st.download_button(
            label="СКАЧАТЬ EXCEL (.XLSX)",
            data=excel_data,
            file_name=f"Apologet_Report_{period.replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
