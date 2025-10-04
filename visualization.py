import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from scipy import stats

st.set_page_config(page_title="Professional Data Viz Dashboard", layout="wide")
st.title("📊 Professional Data Visualization Dashboard")

# CSV upload
file = st.file_uploader("Upload your CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    
    # Tabs for layout
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Charts", "Correlation", "Trend & Outliers"])
    
    # ================== Tab 1: Overview ==================
    with tab1:
        st.subheader("🔎 Dataset Overview")
        st.write(df.head())
        st.write("Number of rows:", df.shape[0])
        st.write("Number of columns:", df.shape[1])
        
        if st.checkbox("Show Statistical Summary"):
            st.write(df.describe())
    
    # ================== Tab 2: Charts ==================
    with tab2:
        st.subheader("📈 Interactive Charts")
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        x_axis = st.selectbox("Select X axis", numeric_cols)
        y_axis = st.selectbox("Select Y axis", numeric_cols)
        chart_type = st.radio("Select chart type:", ("Line Chart", "Bar Chart", "Scatter Plot"))
        
        if chart_type == "Line Chart":
            fig = px.line(df, x=x_axis, y=y_axis, markers=True)
        elif chart_type == "Bar Chart":
            fig = px.bar(df, x=x_axis, y=y_axis)
        else:
            fig = px.scatter(df, x=x_axis, y=y_axis)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ================== Tab 3: Correlation ==================
    with tab3:
        st.subheader("🌡️ Correlation Heatmap & Pairplot")
        corr = df.corr()
        fig, ax = plt.subplots(figsize=(8,6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
        
        if st.checkbox("Show Pairplot"):
            pair_fig = sns.pairplot(df[numeric_cols])
            st.pyplot(pair_fig)
    
    # ================== Tab 4: Trend & Outliers ==================
    with tab4:
        st.subheader("🔍 Trend & Outlier Detection")
        col = st.selectbox("Select column for trend/outlier analysis", numeric_cols)
        
        # Rolling mean trend
        window = st.slider("Select rolling window size", min_value=1, max_value=20, value=3)
        df['Rolling Mean'] = df[col].rolling(window).mean()
        
        fig, ax = plt.subplots(figsize=(8,5))
        ax.plot(df.index, df[col], label=col, marker='o')
        ax.plot(df.index, df['Rolling Mean'], label='Rolling Mean', linestyle='--')
        ax.set_title(f"{col} with Rolling Mean Trend")
        ax.legend()
        st.pyplot(fig)
        
        # Outlier detection using z-score
        z_scores = np.abs(stats.zscore(df[col].dropna()))
        outliers = df[col][z_scores > 3]
        if not outliers.empty:
            st.write("Outliers detected:")
            st.write(outliers)
        else:
            st.write("No outliers detected.")
