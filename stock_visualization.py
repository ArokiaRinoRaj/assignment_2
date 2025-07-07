import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from urllib.parse import quote_plus

# DB connection
def get_engine():
    user = 'rino'
    password = quote_plus('admin@123')
    host = 'localhost'
    port = 3306
    database = 'mydb'
    return create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

engine = get_engine()

st.title("Stock Market Analysis Dashboard")

option = st.sidebar.selectbox(
    "Choose Analysis Type",
    [
        "1. Volatility Analysis",
        "2. Cumulative Returns",
        "3. Sector Performance",
        "4. Price Correlation",
        "5. Monthly Gainers & Losers"
    ]
)

# 1. Volatility
if option.startswith("1"):
    st.subheader("Top 10 Most Volatile Stocks")
    df = pd.read_sql("SELECT * FROM stock_volatility ORDER BY volatility DESC LIMIT 10", engine)
    df['volatility'] = df['volatility'] * 100
    df['volatility'] = df['volatility'].round(2)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='ticker', y='volatility', data=df, ax=ax, palette="Reds_r")
    ax.set_title("Volatility of Top 10 Stocks")
    ax.set_xlabel("stock")
    ax.set_ylabel("volatility %")
    plt.xticks(rotation=45)
    st.pyplot(fig)

#  2. Cumulative Returns
elif option.startswith("2"):
    st.subheader("Top 5 Stocks by Cumulative Return")
    df = pd.read_sql("SELECT * FROM cumulative_returns ORDER BY cumulative_return DESC LIMIT 5", engine)
    df['cumulative_return'] = (df['cumulative_return'] * 100).round(2)
    fig = px.bar(df, x="ticker", y="cumulative_return", color="ticker", title="Cumulative Returns")
    fig.update_layout(
        xaxis_title="Stocks",
        yaxis_title="Cumulative Return (%)",
        xaxis_tickangle=45
    )
    st.plotly_chart(fig)

# 3. Sector Performance
elif option.startswith("3"):
    st.subheader("Sector-wise Average Returns")
    df = pd.read_sql("SELECT * FROM sector_performance ORDER BY average_return DESC", engine)
    df['average_return'] = (df['average_return'] * 100).round(2)
    fig = px.bar(df, x='sector', y='average_return', color='sector', title="Average Yearly Return by Sector")
    fig.update_layout(
        xaxis_title="Sector",
        yaxis_title="Average Return (%)",
        xaxis_tickangle=45
    )
    st.plotly_chart(fig)

# 4. Correlation Heatmap
elif option.startswith("4"):
    st.subheader("Stock Price Correlation")
    df = pd.read_sql("SELECT * FROM daily_returns", engine)
    df['date'] = pd.to_datetime(df['date'])
    wide_df = df.pivot(index='date', columns='ticker', values='daily_return')
    corr_matrix = wide_df.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, cmap="coolwarm", annot=False)
    st.pyplot(fig)

# 5. Monthly Gainers & Losers
elif option.startswith("5"):
    st.subheader("Monthly Gainers & Losers")
    df = pd.read_sql("SELECT * FROM monthly_performance", engine)
    df['month'] = pd.to_datetime(df['month'])

    selected_month = st.selectbox("Select Month", df['month'].dt.strftime('%Y-%m').sort_values().unique())

    # Filter month
    filtered = df[df['month'].dt.strftime('%Y-%m') == selected_month]
    top5 = filtered.sort_values('monthly_return', ascending=False).head(5)
    bottom5 = filtered[filtered['monthly_return'] < 0].sort_values('monthly_return').head(5)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(top5, x='ticker', y='monthly_return', color='ticker', title='Top 5 Gainers')
        fig.update_layout(
        xaxis_title="Stocks",
        yaxis_title="Monthly Return (%)"
        )
        st.plotly_chart(fig)

    with col2:
        fig = px.bar(bottom5, x='ticker', y='monthly_return', color='ticker', title='Top 5 Losers')
        fig.update_layout(
        xaxis_title="Stocks",
        yaxis_title="Monthly Return (%)"
        )
        st.plotly_chart(fig)
