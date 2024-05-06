import sqlite3

# Подключение к базе данных SQLite
connection = sqlite3.connect('database.db')

# Создание курсора
cur = connection.cursor()

# Создание таблицы items
cur.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    status TEXT NOT NULL,
    time DATE
)
""")

# Создание таблицы item_positions
cur.execute("""
CREATE TABLE IF NOT EXISTS item_positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    position TEXT NOT NULL,
    unit TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (item_id) REFERENCES items(id)
)
""")

# Создание таблицы recipients
cur.execute("""
CREATE TABLE IF NOT EXISTS recipients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

# Создание таблицы products
cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

# Вставка данных в таблицу items
cur.execute("INSERT INTO items (title, company, status) VALUES (?, ?, ?)",
            ('Накладная №1 от 25.05.2022', 'Авангард Групп', 'не выдан'))
cur.execute("INSERT INTO items (title, company, status) VALUES (?, ?, ?)",
            ('Накладная №2 от 25.05.2022', 'Браво Групп', 'не выдан'))

# Пример вставки данных в таблицу item_positions
cur.execute("INSERT INTO item_positions (item_id, position, unit, quantity) VALUES (?, ?, ?, ?)",
            (1, 'Товар А', 'шт', 100))
cur.execute("INSERT INTO item_positions (item_id, position, unit, quantity) VALUES (?, ?, ?, ?)",
            (2, 'Товар B', 'кг', 50))

recipients = [
    ('ООО "Поставщик 1"',),
    ('ИП Иванов',),
    ('АО "Покупатель 2"',),
    ('ТОО "Грузополучатель 3"',)
]
cur.executemany("INSERT INTO recipients (name) VALUES (?)", recipients)

# Добавление данных о товарах
products = [
    ('Товар 1',),
    ('Товар 2',),
    ('Товар 3',),
    ('Товар 4',),
    ('Товар 5',),
]
cur.executemany("INSERT INTO products (name) VALUES (?)", products)

# Фиксация изменений
connection.commit()

# Закрытие соединения
connection.close()
