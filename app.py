import sqlite3
from flask import Flask, render_template, abort

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('index.html', items=items)


@app.route('/<int:item_id>')
def item(item_id):
    item = get_item(item_id)
    return render_template('item.html', item=item)


def get_item(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    conn.close()
    if item is None:
        abort(404)
    return item


if __name__ == '__main__':
    app.run()
