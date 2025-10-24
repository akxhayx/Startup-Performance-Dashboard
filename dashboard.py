import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Startup Performance Dashboard", layout="wide")
st.title("📊 Startup Performance Dashboard")

uploaded_file = st.file_uploader("Upload your startup dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head())

    # Dropdowns
    metric = st.selectbox("Select Metric to Compare:", ["Revenue_Monthly", "Expenses"])
    trend_filter = st.selectbox("Filter by Impact:", ["All", "Benefited", "Hurt", "Neutral"])

    if trend_filter != "All":
        df = df[df["Impact"] == trend_filter]

    # Plot
    x = np.arange(len(df["Startup"]))
    width = 0.35
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(x - width / 2, df["Revenue_Monthly"], width, label="Revenue", color="green")
    ax.bar(x + width / 2, df["Expenses"], width, label="Expenses", color="red")
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels(df["Startup"], rotation=90)
    ax.set_xlabel("Startup")
    ax.set_ylabel("Amount (INR, Log Scale)")
    ax.set_title("Revenue vs Expenses per Startup (Log Scale, Side-by-Side)")
    ax.legend()

    st.pyplot(fig)

    # Pie Chart for Impact
    impact_counts = df["Impact"].value_counts()
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    colors = {"Benefited": "green", "Hurt": "red", "Neutral": "gray"}
    ax2.pie(impact_counts, labels=impact_counts.index, autopct="%1.1f%%",
            colors=[colors[i] for i in impact_counts.index], startangle=140)
    ax2.set_title("Impact of Trend on Startups")
    st.pyplot(fig2)
