import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random


def scrape_steam_games(pages=5):
    base_url = "https://store.steampowered.com/search/?ignore_preferences=1&page="
    games_data = []

    for page in range(1, pages + 1):
        url = base_url + str(page)
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')

        games = soup.find_all('a', class_='search_result_row')

        for game in games:
            title = game.find('span', class_='title').text

            # Получаем цену
            price_block = game.find('div', class_='discount_final_price')
            if not price_block:
                price_block = game.find('div', class_='search_price')
            price = price_block.text.strip() if price_block else 'N/A'

            # Получаем числовое значение цены
            try:
                numeric_price = float(''.join(c for c in price if c.isdigit() or c == ',').replace(',', '.'))
            except:
                numeric_price = 0.0  # Для бесплатных игр

            # Получаем рейтинг
            rating_block = game.find('div', class_='search_review_summary')
            if rating_block:
                rating_str = rating_block.get('data-tooltip-html', '').split('%')[0]
                try:
                    rating = int(rating_str)
                except:
                    rating = None
            else:
                rating = None

            games_data.append({
                'title': title,
                'price': price,
                'numeric_price': numeric_price,
                'rating': rating,
                'url': game['href']
            })

        # Задержка между запросами
        time.sleep(random.uniform(1, 3))

    return pd.DataFrame(games_data)

def get_game_ratings(df):
    ratings = []

    for url in df['url']:
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')

            # Получаем рейтинг
            rating_block = soup.find('div', class_='user_reviews_summary_row')
            if rating_block:
                rating_text = rating_block.get('data-tooltip-html', '')
                if '%' in rating_text:
                    rating = int(rating_text.split('%')[0])
                else:
                    rating = None
            else:
                rating = None

            ratings.append(rating)
            time.sleep(random.uniform(1, 2))
        except:
            ratings.append(None)

    return ratings




# Собираем данные о 100+ играх (5 страниц по 25 игр)
print("Начинаем сбор данных...")
games_df = scrape_steam_games(pages=5)

# Получаем рейтинги для игр
print("Получаем рейтинги игр...")
games_df['rating'] = get_game_ratings(games_df)

# Сохраняем данные
games_df.to_csv('data/steam_games_ratings.csv', index=False)
print(f"Собрано {len(games_df)} игр. Данные сохранены в data/steam_games_ratings.csv")