import sqlite3

# Подключение к базе данных SQLite
connection = sqlite3.connect('database.db')

# Создание курсора
cur = connection.cursor()

# Создание таблицы items
cur.execute("""
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    status TEXT NOT NULL,
    time DATE
)
""")

# Вставка данных в таблицу
cur.execute("INSERT INTO items (title, company, status) VALUES (?, ?, ?)",
            ('Накладная №1 от 25.05.2022', 'Авангард Групп', 'не выдан'))
cur.execute("INSERT INTO items (title, company, status) VALUES (?, ?, ?)",
            ('Накладная №2 от 25.05.2022', 'Браво Групп', 'не выдан'))

# Фиксация изменений
connection.commit()

# Закрытие соединения
connection.close()
