import os
import sys
import sqlite3
from tkinter import messagebox

def get_db_path():
    """
    Returns a reliable path for the SQLite database file.
    If running as EXE (PyInstaller), stores database under user's Documents folder for persistence.
    Otherwise uses project 'data/' folder.
    """
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller bundle (EXE)
        docs_path = os.path.join(os.path.expanduser('~'), 'Documents', 'EmployeeManagementSystem', 'data')
        os.makedirs(docs_path, exist_ok=True)
        return os.path.join(docs_path, "emp_data.db")
    else:
        # Running as Python script
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, "emp_data.db")

db_path = get_db_path()

print("Using database at:", db_path)  # For debug - remove in production

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

    if option == 'Salary':
        # Exact case-sensitive match for salary
        cursor.execute(f"SELECT * FROM data WHERE {option} = ?", (value,))
    else:
        # Case-insensitive search for other columns
        cursor.execute(f"SELECT * FROM data WHERE LOWER({option}) = LOWER(?)", (value.lower(),))

    return cursor.fetchall()

def delete_all_records():
    cursor.execute('DELETE FROM data')
    conn.commit()
