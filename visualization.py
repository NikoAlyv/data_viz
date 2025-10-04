import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 Smart Data Vizualizasiya App")

# CSV yükləmə
file = st.file_uploader("CSV faylını yüklə", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    st.subheader("🔎 Dataset Önizləmə")
    st.write(df.head())

    # Statistical summary
    if st.checkbox("📈 Statistical Summary"):
        st.subheader("Statistics")
        st.write(df.describe())

    # Heatmap
    if st.checkbox("🌡️ Correlation Heatmap"):
        st.subheader("Correlation Heatmap")
        plt.figure(figsize=(8,6))
        sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
        st.pyplot(plt.gcf())

    # Sidebar parametrləri
    st.sidebar.header("⚙️ Vizualizasiya parametrləri")
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    x_axis = st.sidebar.selectbox("X oxu seç", numeric_cols)
    y_axis = st.sidebar.selectbox("Y oxu seç", numeric_cols)

    chart_type = st.sidebar.radio(
        "Qrafik növünü seç:",
        ("Line Chart", "Bar Chart", "Scatter Plot")
    )

    # Outlier və trend üçün simple analysis
    if st.checkbox("🔍 Outlier / Trend Analysis"):
        st.subheader("Outlier və Trend Analysis")
        q1 = df[y_axis].quantile(0.25)
        q3 = df[y_axis].quantile(0.75)
        iqr = q3 - q1
        outliers = df[(df[y_axis] < q1 - 1.5*iqr) | (df[y_axis] > q3 + 1.5*iqr)]
        if not outliers.empty:
            st.write("Outliers:")
            st.write(outliers)
        else:
            st.write("Outliers tapılmadı.")

    # Çizim
    plt.figure(figsize=(8,5))
    if chart_type == "Line Chart":
        sns.lineplot(x=x_axis, y=y_axis, data=df, marker="o")
    elif chart_type == "Bar Chart":
        sns.barplot(x=x_axis, y=y_axis, data=df, palette="viridis")
    else:
        sns.scatterplot(x=x_axis, y=y_axis, data=df, s=100, color="red")

    st.pyplot(plt.gcf())
