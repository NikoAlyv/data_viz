import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 Interaktiv Data Vizualizasiya App")

# CSV yükləmə
file = st.file_uploader("CSV faylını yüklə", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    st.subheader("🔎 Dataset Önizləmə")
    st.write(df.head())

    # İstifadəçiyə kolon seçimi ver
    st.sidebar.header("⚙️ Vizualizasiya parametrləri")
    x_axis = st.sidebar.selectbox("X oxu seç", df.columns)
    y_axis = st.sidebar.selectbox("Y oxu seç", df.columns)

    # Qrafik növü seçmək
    chart_type = st.sidebar.radio(
        "Qrafik növünü seç:",
        ("Line Chart", "Bar Chart", "Scatter Plot")
    )

    # Çizim
    plt.figure(figsize=(8,5))
    if chart_type == "Line Chart":
        sns.lineplot(x=x_axis, y=y_axis, data=df, marker="o")
    elif chart_type == "Bar Chart":
        sns.barplot(x=x_axis, y=y_axis, data=df, palette="viridis")
    else:
        sns.scatterplot(x=x_axis, y=y_axis, data=df, s=100, color="red")

    st.pyplot(plt.gcf())
