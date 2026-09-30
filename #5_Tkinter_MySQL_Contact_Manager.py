"""Q5: Tkinter contact manager backed by MySQL.

Install: python -m pip install mysql-connector-python
Create a database first, then set DB_CONFIG below or enter credentials at launch.
"""
import re
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

try:
    import mysql.connector
except ImportError:
    mysql = None
else:
    mysql = mysql.connector

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


class ContactManager:
    def __init__(self, root, connection):
        self.root, self.connection = root, connection
        self.root.title("Contact Manager")
        self.root.geometry("900x560")
        self.selected_id = None
        self.create_table()
        self.build_ui()
        self.refresh()

    def create_table(self):
        cur = self.connection.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS Contact (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(150) NOT NULL,
            email VARCHAR(254) NOT NULL UNIQUE,
            phone VARCHAR(40),
            category VARCHAR(80),
            notes TEXT,
            INDEX idx_contact_name(name)
        )""")
        self.connection.commit()
        cur.close()

    def build_ui(self):
        form = ttk.LabelFrame(self.root, text="Contact details", padding=10)
        form.pack(fill="x", padx=10, pady=8)
        self.vars = {key: tk.StringVar() for key in ("name", "email", "phone", "category")}
        for col, (key, var) in enumerate(self.vars.items()):
            ttk.Label(form, text=key.title()).grid(row=0, column=col, sticky="w")
            ttk.Entry(form, textvariable=var, width=24).grid(row=1, column=col, padx=4)
        ttk.Label(form, text="Notes").grid(row=0, column=4, sticky="w")
        self.notes = tk.Text(form, width=25, height=3)
        self.notes.grid(row=1, column=4, padx=4)
        actions = ttk.Frame(self.root); actions.pack(fill="x", padx=10)
        for label, command in [("Add", self.add), ("Update", self.update), ("Delete", self.delete),
                               ("Clear", self.clear), ("Refresh", self.refresh)]:
            ttk.Button(actions, text=label, command=command).pack(side="left", padx=3)
        self.search_var = tk.StringVar()
        ttk.Entry(actions, textvariable=self.search_var, width=24).pack(side="left", padx=(15, 3))
        ttk.Button(actions, text="Search", command=self.search).pack(side="left")
        self.table = ttk.Treeview(self.root, columns=("id","name","email","phone","category","notes"),
                                  show="headings")
        for col in ("id","name","email","phone","category","notes"):
            self.table.heading(col, text=col.title())
            self.table.column(col, width=120)
        self.table.pack(fill="both", expand=True, padx=10, pady=10)
        self.table.bind("<<TreeviewSelect>>", self.select)

    def values(self):
        data = {key: var.get().strip() for key, var in self.vars.items()}
        data["notes"] = self.notes.get("1.0", "end").strip()
        if not data["name"] or not EMAIL_RE.fullmatch(data["email"]):
            raise ValueError("Enter a name and a valid email address.")
        return data

    def run(self, sql, params=()):
        cur = self.connection.cursor()
        cur.execute(sql, params)
        self.connection.commit()
        cur.close()

    def add(self):
        try:
            d = self.values()
            self.run("INSERT INTO Contact(name,email,phone,category,notes) VALUES(%s,%s,%s,%s,%s)",
                     tuple(d[k] for k in ("name","email","phone","category","notes")))
            self.refresh(); self.clear()
        except Exception as exc:
            messagebox.showerror("Cannot add contact", str(exc))

    def update(self):
        if self.selected_id is None:
            messagebox.showinfo("Select", "Select a contact first."); return
        try:
            d = self.values()
            self.run("UPDATE Contact SET name=%s,email=%s,phone=%s,category=%s,notes=%s WHERE id=%s",
                     tuple(d[k] for k in ("name","email","phone","category","notes")) + (self.selected_id,))
            self.refresh()
        except Exception as exc:
            messagebox.showerror("Cannot update contact", str(exc))

    def delete(self):
        if self.selected_id is None: return
        if messagebox.askyesno("Confirm", "Delete selected contact?"):
            self.run("DELETE FROM Contact WHERE id=%s", (self.selected_id,))
            self.refresh(); self.clear()

    def search(self):
        term = "%" + self.search_var.get().strip() + "%"
        self.populate("SELECT id,name,email,phone,category,notes FROM Contact WHERE name LIKE %s OR email LIKE %s OR phone LIKE %s ORDER BY name",
                      (term, term, term))

    def refresh(self):
        self.populate("SELECT id,name,email,phone,category,notes FROM Contact ORDER BY name")

    def populate(self, sql, params=()):
        for item in self.table.get_children(): self.table.delete(item)
        cur = self.connection.cursor()
        cur.execute(sql, params)
        for row in cur.fetchall(): self.table.insert("", "end", values=row)
        cur.close()

    def select(self, _event=None):
        selected = self.table.selection()
        if not selected: return
        row = self.table.item(selected[0], "values")
        self.selected_id = int(row[0])
        for key, value in zip(self.vars, row[1:5]): self.vars[key].set(value or "")
        self.notes.delete("1.0", "end"); self.notes.insert("1.0", row[5] or "")

    def clear(self):
        self.selected_id = None
        for var in self.vars.values(): var.set("")
        self.notes.delete("1.0", "end")
        self.table.selection_remove(self.table.selection())


def main():
    if mysql is None:
        print("Install dependency: python -m pip install mysql-connector-python"); return
    host = input("MySQL host [localhost]: ").strip() or "localhost"
    user = input("MySQL user: ").strip()
    password = input("MySQL password: ")
    database = input("Database: ").strip()
    try:
        connection = mysql.connect(host=host, user=user, password=password, database=database)
    except Exception as exc:
        print("Database connection failed:", exc); return
    root = tk.Tk()
    app = ContactManager(root, connection)
    root.mainloop()
    connection.close()


if __name__ == "__main__":
    main()
