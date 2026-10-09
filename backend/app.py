from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import datetime

from database import get_db, init_db
from voice_service import parse_voice_command
from printer_service import PrinterService

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
CORS(app)

if os.environ.get('VERCEL'):
    # Ensure the database is initialized on Vercel serverless cold start
    init_db()

from flask import redirect

# --- ROUTES: Frontend ---
@app.route('/')
def index():
    return redirect('/dashboard')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/billing')
def billing():
    return render_template('billing.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/stock')
def stock():
    return render_template('stock.html')

@app.route('/bills')
def bills():
    return render_template('bills.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/bill/<int:id>/view')
def print_bill_view(id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM bills WHERE id=?", (id,))
    row = c.fetchone()
    if not row:
        return "Bill not found", 404
    bill = dict(row)
    
    c.execute('''SELECT bi.*, p.name FROM bill_items bi 
                 JOIN products p ON bi.product_id = p.id 
                 WHERE bi.bill_id=?''', (id,))
    items = [dict(row) for row in c.fetchall()]
    
    c.execute("SELECT key, value FROM settings")
    shop_settings = {row['key']: row['value'] for row in c.fetchall()}
    conn.close()
    
    return render_template('print_template.html', bill=bill, items=items, settings=shop_settings)


# --- ROUTES: API ---
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    if data.get('username') == 'admin' and data.get('password') == 'admin123':
        return jsonify({"status": "success", "token": "fake-jwt-token"})
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@app.route('/api/dashboard', methods=['GET'])
def api_dashboard():
    conn = get_db()
    c = conn.cursor()
    
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    c.execute("SELECT SUM(grand_total), COUNT(id) FROM bills WHERE date(created_at) = ?", (today,))
    sales_data = c.fetchone()
    today_sales = sales_data[0] or 0
    today_bills = sales_data[1] or 0
    
    c.execute("SELECT COUNT(id) FROM products")
    total_products = c.fetchone()[0] or 0
    
    c.execute("SELECT COUNT(id) FROM products WHERE stock_quantity <= minimum_stock")
    low_stock = c.fetchone()[0] or 0
    
    conn.close()
    return jsonify({
        "today_sales": today_sales,
        "today_bills": today_bills,
        "total_products": total_products,
        "low_stock_products": low_stock
    })

@app.route('/api/products', methods=['GET', 'POST'])
def api_products():
    conn = get_db()
    c = conn.cursor()
    
    if request.method == 'GET':
        c.execute("SELECT * FROM products")
        prods = [dict(row) for row in c.fetchall()]
        
        # Get aliases
        for p in prods:
            c.execute("SELECT alias FROM product_aliases WHERE product_id = ?", (p['id'],))
            p['aliases'] = [row['alias'] for row in c.fetchall()]
            
        conn.close()
        return jsonify(prods)
        
    elif request.method == 'POST':
        data = request.json
        c.execute('''INSERT INTO products (name, category, unit, price, gst_percentage, stock_quantity, minimum_stock) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (data['name'], data['category'], data['unit'], data['price'], 
                   data.get('gst_percentage', 0), data.get('stock_quantity', 0), data.get('minimum_stock', 0)))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})

@app.route('/api/products/<int:id>', methods=['PUT', 'DELETE'])
def api_product(id):
    conn = get_db()
    c = conn.cursor()
    
    if request.method == 'PUT':
        data = request.json
        c.execute('''UPDATE products SET name=?, category=?, unit=?, price=?, gst_percentage=?, stock_quantity=?, minimum_stock=? 
                     WHERE id=?''',
                  (data['name'], data['category'], data['unit'], data['price'], 
                   data.get('gst_percentage', 0), data.get('stock_quantity', 0), data.get('minimum_stock', 0), id))
        conn.commit()
    elif request.method == 'DELETE':
        c.execute("DELETE FROM products WHERE id=?", (id,))
        c.execute("DELETE FROM product_aliases WHERE product_id=?", (id,))
        conn.commit()
        
    conn.close()
    return jsonify({"status": "success"})

@app.route('/api/voice/parse', methods=['POST'])
@app.route('/api/process-voice', methods=['POST'])
def api_voice_parse():
    data = request.json
    text = data.get('text', '')
    
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    prods = [dict(row) for row in c.fetchall()]
    for p in prods:
        c.execute("SELECT alias FROM product_aliases WHERE product_id = ?", (p['id'],))
        p['aliases'] = [row['alias'] for row in c.fetchall()]
    conn.close()
    
    result = parse_voice_command(text, prods)
    return jsonify(result)

@app.route('/api/bills', methods=['GET', 'POST'])
def api_bills():
    conn = get_db()
    c = conn.cursor()
    
    if request.method == 'POST':
        data = request.json
        # Generate bill number
        bill_number = f"BILL-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        c.execute('''INSERT INTO bills (bill_number, subtotal, discount, gst, grand_total, payment_method) 
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (bill_number, data['subtotal'], data.get('discount', 0), data['gst'], data['grand_total'], data.get('payment_method', 'CASH')))
        
        bill_id = c.lastrowid
        
        for item in data['items']:
            c.execute('''INSERT INTO bill_items (bill_id, product_id, quantity, unit, price, total) 
                         VALUES (?, ?, ?, ?, ?, ?)''',
                      (bill_id, item['product_id'], item['quantity'], item['unit'], item['price'], item['total']))
            # Reduce stock
            c.execute("UPDATE products SET stock_quantity = stock_quantity - ? WHERE id = ?", (item['quantity'], item['product_id']))
            
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "bill_id": bill_id, "bill_number": bill_number})
        
    elif request.method == 'GET':
        c.execute("SELECT * FROM bills ORDER BY id DESC")
        bills = [dict(row) for row in c.fetchall()]
        conn.close()
        return jsonify(bills)

@app.route('/api/bills/<int:id>', methods=['GET'])
def api_bill(id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM bills WHERE id=?", (id,))
    bill = dict(c.fetchone())
    
    c.execute('''SELECT bi.*, p.name FROM bill_items bi 
                 JOIN products p ON bi.product_id = p.id 
                 WHERE bi.bill_id=?''', (id,))
    items = [dict(row) for row in c.fetchall()]
    
    conn.close()
    return jsonify({"bill": bill, "items": items})

@app.route('/api/bills/<int:id>/print', methods=['POST'])
def api_bill_print(id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM bills WHERE id=?", (id,))
    bill = dict(c.fetchone())
    
    c.execute('''SELECT bi.*, p.name FROM bill_items bi 
                 JOIN products p ON bi.product_id = p.id 
                 WHERE bi.bill_id=?''', (id,))
    items = [dict(row) for row in c.fetchall()]
    
    c.execute("SELECT key, value FROM settings")
    settings = {row['key']: row['value'] for row in c.fetchall()}
    
    conn.close()
    
    printer = PrinterService(printer_name=settings.get('printer_name'))
    printer.print_bill(bill, items, settings)
    
    return jsonify({"status": "success"})

@app.route('/api/stock', methods=['GET'])
def api_stock():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, name, category, stock_quantity, minimum_stock, unit FROM products")
    stock = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(stock)

@app.route('/api/stock/<int:id>', methods=['PUT'])
def api_update_stock(id):
    data = request.json
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE products SET stock_quantity=? WHERE id=?", (data['stock_quantity'], id))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/api/settings', methods=['GET', 'PUT'])
def api_settings():
    conn = get_db()
    c = conn.cursor()
    if request.method == 'GET':
        c.execute("SELECT * FROM settings")
        settings = {row['key']: row['value'] for row in c.fetchall()}
        conn.close()
        return jsonify(settings)
    elif request.method == 'PUT':
        data = request.json
        for k, v in data.items():
            c.execute("UPDATE settings SET value=? WHERE key=?", (v, k))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})


# Service Worker & Manifest
@app.route('/service-worker.js')
def service_worker():
    return app.send_static_file('../service-worker.js')

@app.route('/manifest.json')
def manifest():
    return app.send_static_file('../manifest.json')

if __name__ == '__main__':
    # Ensure db directory exists
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'database'), exist_ok=True)
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
