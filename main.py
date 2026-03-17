import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# وظيفة لإنشاء قاعدة البيانات إذا لم تكن موجودة
def init_db():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                      (id INTEGER PRIMARY KEY, player_id TEXT, amount TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/charge', methods=['POST'])
def charge():
    player_id = request.form.get('player_id')
    return render_template('charge.html', player_id=player_id)

@app.route('/checkout', methods=['POST'])
def checkout():
    user_id = request.form.get('user_id')
    amount = request.form.get('amount')
    
    # حفظ الطلب في قاعدة البيانات
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (player_id, amount) VALUES (?, ?)", (user_id, amount))
    conn.commit()
    conn.close()
    
    return f"<h3>تم إتمام الطلب بنجاح!</h3><a href='/'>العودة للرئيسية</a>"

# لوحة التحكم الاحترافية لعرض البيانات كجدول
@app.route('/admin')
def admin():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    conn.close()
    
    # تنسيق الجدول باستخدام Bootstrap
    table_rows = ""
    for row in rows:
        table_rows += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    
    return f'''
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <div class="container mt-5">
        <h2>سجل طلبات الشحن</h2>
        <table class="table table-bordered table-striped">
            <thead class="table-dark">
                <tr><th>رقم الطلب</th><th>الـ ID</th><th>الكمية (شدة)</th></tr>
            </thead>
            <tbody>{table_rows}</tbody>
        </table>
        <a href='/' class='btn btn-primary'>العودة للرئيسية</a>
    </div>
    '''

if __name__ == '__main__':
    # أضفنا host و port ليتناسب مع سيرفرات Render
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)