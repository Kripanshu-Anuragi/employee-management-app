import os
import sys
import sqlite3
from tkinter import messagebox

def resource_path(rel_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.normpath(os.path.join(base_path, rel_path))

db_folder = resource_path("data")
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, "emp_data.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS data (
    id TEXT PRIMARY KEY,
    Name TEXT,
    Phone TEXT,
    Role TEXT,
    Gender TEXT,
    Salary REAL
)
''')
conn.commit()

def insert_data(id, name, phone_number, role, gender, salary):
    try:
        cursor.execute('INSERT INTO data (id, Name, Phone, Role, Gender, Salary) VALUES (?, ?, ?, ?, ?, ?)',
                       (id, name, phone_number, role, gender, salary))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror('Error', 'Employee ID already exists.')
    except Exception as e:
        messagebox.showerror('Error', f'Insert failed: {e}')

def id_exists(id):
    cursor.execute('SELECT COUNT(*) FROM data WHERE id = ?', (id,))
    result = cursor.fetchone()
    return result[0] > 0

def fetch_employees():
    cursor.execute('SELECT * FROM data')
    result = cursor.fetchall()
    def emp_id_num(emp):
        try:
            return int(emp[0][3:])
        except:
            return 0
    return sorted(result, key=emp_id_num)

def update(id, new_name, new_phone_number, new_role, new_gender, new_salary):
    cursor.execute('''
        UPDATE data SET Name=?, Phone=?, Role=?, Gender=?, Salary=? WHERE id=?
    ''', (new_name, new_phone_number, new_role, new_gender, new_salary, id))
    conn.commit()

def delete(id):
    cursor.execute('DELETE FROM data WHERE id=?', (id,))
    conn.commit()

def search(option, value):
    allowed_columns = ['id', 'Name', 'Phone', 'Role', 'Gender', 'Salary']
    if option not in allowed_columns:
        messagebox.showerror('Error', 'Invalid search option.')
        return []

    # For numeric fields like Salary, keep case sensitive exact match
    if option == 'Salary':
        query = f"SELECT * FROM data WHERE {option} = ?"
        cursor.execute(query, (value,))
    else:
        # Case-insensitive search using LOWER()
        query = f"SELECT * FROM data WHERE LOWER({option}) = LOWER(?)"
        cursor.execute(query, (value,))

    return cursor.fetchall()


def delete_all_records():
    cursor.execute('DELETE FROM data')
    conn.commit()
