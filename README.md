
# Анализ игр Steam: цены и рейтинги

## Авторы Скрипюк Дарья, Пешкова Алина


Проект анализирует взаимосвязь между ценами и рейтингами игр в Steam.

## Функционал
- Сбор данных о играх с Steam
- Анализ распределения рейтингов
- Визуализация зависимости цены от рейтинга
- Интерактивный дашборд

##  Установка
 1. Клонируйте репозиторий:
 git clone https://github.com/dskripyuk/steam-games-analysis.git
 cd steam-games-analysis
 2. Установите зависимости:
 pip install -r requirements.txt

##  Использование

1. Сбор данных (100+ игр):
python scripts/script.py

2. Запуск анализа:
jupyter notebook notebooks/analysis.ipynb

3. Запуск дашборда:
streamlit run dashboard/app.py
