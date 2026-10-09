import sqlite3
import os

if os.environ.get('VERCEL'):
    DB_PATH = '/tmp/voicebill.db'
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'voicebill.db')
    
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')
SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'seed.sql')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    
    # Check if we need to seed
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        print("Seeding database...")
        with open(SEED_PATH, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
            
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
