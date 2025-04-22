import sqlite3
import bcrypt
from datetime import datetime, timedelta
import pandas as pd

DATABASE = 'expense_tracker.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Create expenses table
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            tags TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db():
    return sqlite3.connect(DATABASE)

def create_user(username, password):
    try:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        with get_db() as conn:
            conn.execute('''
                INSERT INTO users (username, password) VALUES (?, ?)
            ''', (username, hashed))
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        return False

def authenticate_user(username, password):
    try:
        with get_db() as conn:
            user = conn.execute('''
                SELECT id, password FROM users WHERE username = ?
            ''', (username,)).fetchone()
        
        if user and bcrypt.checkpw(password.encode(), user[1]):
            return user[0]  # Return user ID
        return None
    except Exception as e:
        print(f"Error authenticating user: {str(e)}")
        return None

def add_transaction(user_id, amount, category, description, date, trans_type, tags=None):
    try:
        with get_db() as conn:
            conn.execute('''
                INSERT INTO expenses (user_id, amount, category, description, date, type, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, amount, category, description, date.strftime('%Y-%m-%d')
, trans_type, tags))
            conn.commit()
        return True
    except Exception as e:
        print(f"Error adding transaction: {str(e)}")
        return False

def get_transactions(user_id, start_date=None, end_date=None):
    try:
        with get_db() as conn:
            query = '''
                SELECT id, date, type, category, amount, description, tags 
                FROM expenses 
                WHERE user_id = ?
            '''
            params = [user_id]
            
            if start_date and end_date:
                query += ' AND date BETWEEN ? AND ?'
                params.extend([start_date, end_date])
            
            query += ' ORDER BY date DESC'
            
            return pd.read_sql(query, conn, params=params)
    except Exception as e:
        print(f"Error getting transactions: {str(e)}")
        return pd.DataFrame()

def delete_transaction(transaction_id):
    try:
        with get_db() as conn:
            conn.execute('DELETE FROM expenses WHERE id = ?', (transaction_id,))
            conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting transaction: {str(e)}")
        return False

def update_transaction(transaction_id, amount, category, description, date, trans_type, tags=None):
    try:
        with get_db() as conn:
            conn.execute('''
                UPDATE expenses 
                SET amount = ?, category = ?, description = ?, date = ?, type = ?, tags = ?
                WHERE id = ?
            ''', (amount, category, description, date.strftime('%Y-%m-%d')
, trans_type, tags, transaction_id))
            conn.commit()
        return True
    except Exception as e:
        print(f"Error updating transaction: {str(e)}")
        return False