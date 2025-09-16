import tkinter as tk
import sqlite3, os

db_path = "db3.db"

if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE rest(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
)
''')

cursor.execute('''
INSERT INTO rest (name, age) VALUES
('Artem', 15),
('Denys', 72),
('Egor', 90),
('Charlie', 12),
('Jenny', 9)
''')

conn.commit()


root = tk.Tk()
root.title("Список користувачів")
root.geometry("400x400")

def load_users():
    listbox_users.delete(0, tk.END)
    cursor.execute("SELECT id, name, age FROM rest")
    for row in cursor.fetchall():
        listbox_users.insert(tk.END, f"{row[0]}: {row[1]}, {row[2]} років")

def add():
    name = entry_name.get()
    age = entry_age.get()
    if name and age.isdigit():
        cursor.execute("INSERT INTO rest (name, age) VALUES (?, ?)", (name, int(age)))
        conn.commit()
        load_users()
        entry_name.delete(0, tk.END)
        entry_age.delete(0, tk.END)

def delete():
    selected = listbox_users.curselection()
    if selected:
        user_text = listbox_users.get(selected[0])
        user_id = int(user_text.split(":")[0])
        cursor.execute("DELETE FROM rest WHERE id = ?", (user_id,))
        conn.commit()
        load_users()

def change():
    selected = listbox_users.curselection()
    if selected:
        user_text = listbox_users.get(selected[0])
        user_id = int(user_text.split(":")[0])
        name = entry_name.get()
        age = entry_age.get()
        if name and age.isdigit():
            cursor.execute("UPDATE rest SET name = ?, age = ? WHERE id = ?", (name, int(age), user_id))
            conn.commit()
            load_users()
            entry_name.delete(0, tk.END)
            entry_age.delete(0, tk.END)

# Список
tk.Label(root, text="Список users:").grid(row=5, column=0, columnspan=3, sticky="w", padx=10, pady=(10, 0))
listbox_users = tk.Listbox(root, width=40)
listbox_users.grid(row=6, column=0, columnspan=3, padx=10, pady=(0, 10))

# Поля вводу
tk.Label(root, text="Ім'я:").grid(row=0, column=0, padx=5, pady=5)
tk.Label(root, text="Вік:").grid(row=1, column=0, padx=5, pady=5)

entry_name = tk.Entry(root)
entry_age = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=5, pady=5)
entry_age.grid(row=1, column=1, padx=5, pady=5)

# Кнопки
button_append = tk.Button(root, text="Додати", command=add)
button_append.grid(row=2, column=1, padx=5, pady=10)

button_delete = tk.Button(root, text="Видалити", command=delete)
button_delete.grid(row=3, column=1, padx=5, pady=5)

button_change = tk.Button(root, text="Редагувати", command=change)
button_change.grid(row=4, column=1, padx=5, pady=5)

load_users()

root.mainloop()