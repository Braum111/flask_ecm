from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)


# Функция для подключения к базе данных SQLite
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# Функция для получения списка грузополучателей из базы данных
def get_recipients():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM recipients")
    recipients = cur.fetchall()
    conn.close()
    print("Recipients:", recipients)  # Добавляем вывод в консоль
    return recipients

# Функция для получения списка товаров из базы данных
def get_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM products")
    products = cur.fetchall()
    conn.close()
    print("Products:", products)  # Добавляем вывод в консоль
    return products


# Маршрут для отображения страницы создания новой накладной и обработки POST-запросов
from flask import request


@app.route('/create_invoice', methods=['GET', 'POST'])
def create_invoice():
    if request.method == 'POST':
        recipient_id = request.form.get('recipient')  # Идентификатор грузополучателя
        status = request.form.get('status')
        product_count = int(request.form.get('product_count'))

        print("POST request data:")
        print("Recipient ID:", recipient_id)
        print("Status:", status)
        print("Product count:", product_count)

        conn = get_db_connection()
        cur = conn.cursor()

        # Получаем имя грузополучателя из базы данных
        cur.execute("SELECT name FROM recipients WHERE id=?", (recipient_id,))
        recipient_name = cur.fetchone()[0]

        # Генерируем заголовок накладной
        title = generate_invoice_title()

        # Вставка новой накладной в таблицу items
        cur.execute("INSERT INTO items (title, company, status) VALUES (?, ?, ?)", (title, recipient_name, status))
        item_id = cur.lastrowid

        # Вставка данных о товарах в таблицу item_positions
        for i in range(product_count):
            product_id = int(request.form[f'product_{i}'])
            quantity = int(request.form[f'quantity_{i}'])
            cur.execute("INSERT INTO item_positions (item_id, position, unit, quantity) VALUES (?, ?, ?, ?)",
                        (item_id, product_id, 'шт', quantity))

        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    else:
        recipients = get_recipients()
        products = get_products()
        return render_template('create_invoice.html', recipients=recipients, products=products)

# Функция для генерации заголовка накладной
def generate_invoice_title():
    conn = get_db_connection()
    cur = conn.cursor()

    # Получаем количество существующих накладных
    cur.execute("SELECT COUNT(*) FROM items")
    count = cur.fetchone()[0] + 1

    # Генерируем заголовок с учетом номера и текущей даты
    title = f"Накладная №{count} от {datetime.now().strftime('%d.%m.%Y')}"

    conn.close()
    return title


# Функция для получения имени получателя по его ID
def get_recipient_name(recipient_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM recipients WHERE id = ?", (recipient_id,))
    recipient_name = cur.fetchone()[0]  # Получаем первую (и единственную) строку и первый (и единственный) столбец
    conn.close()
    return recipient_name


# Маршрут для отображения деталей накладной
@app.route('/item/<int:item_id>')
def item(item_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Получение данных о товаре с указанным ID из базы данных
    cur.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item = cur.fetchone()

    # Получение данных о позициях товара из базы данных
    cur.execute("SELECT * FROM item_positions WHERE item_id = ?", (item_id,))
    positions = cur.fetchall()

    conn.close()

    return render_template('item.html', item=item, positions=positions, item_id=item_id)


# Маршрут для отображения списка всех накладных
@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()  # Здесь изменено на 'items'
    conn.close()
    return render_template('index.html', items=items)


@app.route('/issue_item', methods=['POST'])
def issue_item():
    item_id = request.form.get('item_id')

    conn = get_db_connection()
    cur = conn.cursor()

    # Обновление статуса накладной на "выдан"
    cur.execute("UPDATE items SET status = ? WHERE id = ?", ('выдан', item_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
