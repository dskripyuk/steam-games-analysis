import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# Настройка страницы
st.set_page_config(layout="wide")
st.title("Анализ цен и рейтингов игр в Steam")


# Загрузка данных
@st.cache_data
def load_data():
    df = pd.read_csv('data/steam_games_ratings.csv')
    df = df.dropna(subset=['rating']).copy()
    df['price_category'] = pd.cut(df['numeric_price'],
                                  bins=[-1, 0, 10, 20, 50, 100, float('inf')],
                                  labels=['Бесплатно', '0-10$', '10-20$', '20-50$', '50-100$', '100$+'])
    return df


df = load_data()


# Навигация
st.sidebar.title("Навигация")
page = st.sidebar.radio("Выберите раздел:",
                        ["Данные", "Распределение рейтингов", "Цены и рейтинги", "Топ игры"])

if page == "Данные":
    st.header("Исходные данные")
    st.write(f"Всего игр в наборе данных: {len(df)}")

    st.dataframe(df)

    st.download_button(
        label="Скачать данные как CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='steam_games_ratings.csv',
        mime='text/csv'
    )

elif page == "Распределение рейтингов":
    st.header("Распределение рейтингов игр")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Гистограмма распределения")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data=df, x='rating', bins=20, kde=True, ax=ax)
        ax.set_title('Распределение рейтингов')
        ax.set_xlabel('Рейтинг (%)')
        ax.set_ylabel('Количество игр')
        st.pyplot(fig)

    with col2:
        st.subheader("Статистика")
        st.write(f"Средний рейтинг: {df['rating'].mean():.1f}%")
        st.write(f"Медианный рейтинг: {df['rating'].median():.1f}%")
        st.write(f"Минимальный рейтинг: {df['rating'].min()}%")
        st.write(f"Максимальный рейтинг: {df['rating'].max()}%")

elif page == "Цены и рейтинги":
    st.header("Анализ взаимосвязи цен и рейтингов")

    tab1, tab2 = st.tabs(["Зависимость", "По ценовым категориям"])

    with tab1:
        st.subheader("Зависимость цены от рейтинга")

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x='rating', y='numeric_price', alpha=0.6, ax=ax)
        sns.regplot(data=df, x='rating', y='numeric_price', scatter=False, color='red', ax=ax)
        ax.set_title('Цена vs Рейтинг')
        ax.set_xlabel('Рейтинг (%)')
        ax.set_ylabel('Цена (USD)')
        st.pyplot(fig)

        correlation = df['numeric_price'].corr(df['rating'])
        st.write(f"Коэффициент корреляции: {correlation:.2f}")

    with tab2:
        st.subheader("Средний рейтинг по ценовым категориям")

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=df, x='price_category', y='rating', estimator=np.mean, ax=ax)
        ax.set_title('Средний рейтинг по ценовым категориям')
        ax.set_xlabel('Ценовая категория')
        ax.set_ylabel('Средний рейтинг (%)')
        st.pyplot(fig)

elif page == "Топ игры":
    st.header("Лучшие игры по рейтингу")

    top_n = st.slider("Количество игр для отображения", 5, 20, 10)
    top_games = df.sort_values('rating', ascending=False).head(top_n)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Топ-{top_n} игр по рейтингу")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=top_games, x='rating', y='title', palette='viridis', ax=ax)
        ax.set_xlabel('Рейтинг (%)')
        ax.set_ylabel('Название игры')
        st.pyplot(fig)

    with col2:
        st.subheader("Статистика топ-игр")
        st.write(f"Средняя цена: ${top_games['numeric_price'].mean():.2f}")
        st.write(f"Бесплатных игр: {len(top_games[top_games['numeric_price'] == 0])}")
        st.write(f"Самый дорогая игра: ${top_games['numeric_price'].max():.2f}")

        st.dataframe(top_games[['title', 'rating', 'numeric_price']].reset_index(drop=True))