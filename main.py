import sqlite3
import tkinter as tk
from tkinter import Tk
from screeninfo import get_monitors
from tkinter import ttk

def buildDB():

    db = sqlite3.connect("simple.db")
    cursor = db.cursor()

    cursor.execute('''
    DROP TABLE IF EXISTS Students;
    ''')

    cursor.execute('''
    CREATE TABLE Students(
        id integer PRIMARY KEY,
        email TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        lastName TEXT NOT NULL,
        result integer NOT NULL,
        status TEXT
    );
    ''')

    cursor.execute('''
    INSERT INTO Students (id, email, name, lastName, result, status) VALUES
    (1,'s01@wp.pl','Krystian','Matczak',40,'graded'),
    (2,'s02@wp.pl','Malina','Kowalska',55,'graded'),
    (3,'s03@wp.pl','Wojtek','Kowalczuk',60,'mailed'),
    (4,'s04@wp.pl','Eustachy','Nowak',65,'mailed'),
    (5,'s05@wp.pl','Jaroslaw','Kaminski',48,NULL),
    (6,'s06@wp.pl','Robert','Makowski',67, NULL)
    ''')
    cursor.close()
    db.commit()
    db.close()

def fetch_data():
    db = sqlite3.connect("simple.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Students")
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

def load_data():
    data = fetch_data()
    treeview.delete(*treeview.get_children())

    for row in data:
        treeview.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5]))

def open_delete_student_window():
    new_window = tk.Toplevel(root)
    new_window.geometry("120x180")
    new_window.title("Student delete")

    main_label = tk.Label(new_window, text="Usuwanie studenta")
    main_label.pack()

    info_label = tk.Label(new_window, text="Podaj id studenta")
    info_label.pack(pady=10)

    id_entry = tk.Entry(new_window)
    id_entry.pack()

    def delete_student():
        id_delete = id_entry.get()
        sql_command = "DELETE FROM Students WHERE id=?"
        params = (id_delete,)
        try:
            db = sqlite3.connect("simple.db")
            cursor = db.cursor()
            cursor.execute(sql_command, params)
            db.commit()
        except sqlite3.Error as e:
            print(f"Error:  {e}")
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

        load_data()
        new_window.destroy()

    confirm_button = tk.Button(new_window, text="Usun", command=delete_student)
    confirm_button.pack(padx=10, pady=10)


def open_add_student_window():
    new_window = tk.Toplevel(root)
    new_window.geometry("200x250")
    new_window.title("dodawanie studenta")


    email_label = tk.Label(new_window, text="email")
    email_label.pack()

    email_entry = tk.Entry(new_window)
    email_entry.pack()

    name_label = tk.Label(new_window, text="Imie")
    name_label.pack()

    name_entry = tk.Entry(new_window)
    name_entry.pack()

    lastName_label = tk.Label(new_window, text="Nazwisko")
    lastName_label.pack()

    lastName_entry = tk.Entry(new_window)
    lastName_entry.pack()

    result_label = tk.Label(new_window, text="Wynik")
    result_label.pack()

    result_entry = tk.Entry(new_window)
    result_entry.pack()

    status_label = tk.Label(new_window, text="Status")
    status_label.pack()

    status_entry = tk.Entry(new_window)
    status_entry.pack()

    def add_new():
        new_email = email_entry.get()
        new_name = name_entry.get()
        new_lastName = lastName_entry.get()
        new_result = int(result_entry.get())
        new_status= status_entry.get()

        current_data = fetch_data()
        last_id = current_data[len(current_data)-1][0]
        new_id = int(last_id + 1)
        sql_command = "INSERT INTO Students (id, email, name, lastName, result, status) VALUES (?, ?, ?, ?, ?, ?)"
        params = (new_id, new_email, new_name, new_lastName, new_result, new_status)
        try:
            db = sqlite3.connect("simple.db")
            cursor = db.cursor()
            cursor.execute(sql_command, params)
            db.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            db.close()

        load_data()
        new_window.destroy()

    add_button = tk.Button(new_window, text="Dodaj", command=add_new)
    add_button.pack()

def open_details_window(event):
    selected_item = treeview.focus()

    if selected_item:
        item_data = treeview.item(selected_item)
        item_values = item_data["values"]

        details_window = tk.Toplevel(root)
        details_window.title("Szczegóły")

        id_label = ttk.Label(details_window, text="ID:")
        id_label.pack(padx=10)
        id_entry = ttk.Entry(details_window)
        id_entry.insert(0, item_values[0])
        id_entry.config(state="disabled")  # Uniemożliwienie zmiany id
        id_entry.pack(padx=10, pady=10)

        email_label = ttk.Label(details_window, text="Email:")
        email_label.pack(padx=10)
        email_Entry = ttk.Entry(details_window)
        email_Entry.insert(1, item_values[1])
        email_Entry.pack(padx=10, pady=10)

        name_label = ttk.Label(details_window, text="Name:")
        name_label.pack(padx=10)
        name_Entry = ttk.Entry(details_window)
        name_Entry.insert(2, item_values[2])
        name_Entry.pack(padx=10, pady=10)

        lastName_label = ttk.Label(details_window, text="Last name:")
        lastName_label.pack(padx=10)
        lastName_Entry = ttk.Entry(details_window)
        lastName_Entry.insert(3, item_values[3])
        lastName_Entry.pack(padx=10, pady=10)

        result_label = ttk.Label(details_window, text="result:")
        result_label.pack(padx=10)
        result_Entry = ttk.Entry(details_window)
        result_Entry.insert(4, item_values[4])
        result_Entry.pack(padx=10, pady=10)

        status_label = ttk.Label(details_window, text="status:")
        status_label.pack(padx=10)
        status_Entry = ttk.Entry(details_window)
        status_Entry.insert(5, item_values[5])
        status_Entry.pack(padx=10, pady=10)

        def edit_student():
            id = id_entry.get()
            new_email = email_Entry.get()
            new_name = name_Entry.get()
            new_lastName = lastName_Entry.get()
            new_result = int(result_Entry.get())
            new_status = status_Entry.get()

            sql = '''
                UPDATE Students
                SET
                    email = ?,
                    name = ?,
                    lastName = ?,
                    result = ?,
                    status = ?
                WHERE id = ?
            '''
            params = (new_email, new_name, new_lastName, new_result, new_status, id)
            try:
                db = sqlite3.connect("simple.db")
                cursor = db.cursor()
                cursor.execute(sql, params)
                db.commit()
            except sqlite3.Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                db.close()

            load_data()
            details_window.destroy()

        confirm_button = tk.Button(details_window, text="Potwierdź", command=edit_student)
        confirm_button.pack(padx=10, pady=10)

root = Tk()
root.title("PPY 07")

screen_width = get_monitors()[0].width
screen_height = get_monitors()[0].height

# Użyj funkcji buildDB(), aby zresetować tabele Students
buildDB()

treeview= ttk.Treeview(root)
treeview["columns"] = ("id", "email", "name", "lastName", "result", "status")
treeview.column('#0', width=0)
treeview.heading("id", text="ID")
treeview.heading("email", text="Email")
treeview.heading("name", text="Name")
treeview.heading("lastName", text="Last Name")
treeview.heading("result", text="Result")
treeview.heading("status", text="status")
treeview.bind("<Double-1>",open_details_window)
treeview.pack()

add_student_button = tk.Button(root, text="Dodaj studenta", command=open_add_student_window)
add_student_button.pack(side="left")

delete_student_button = tk.Button(root, text="Usun studenta", command=open_delete_student_window)
delete_student_button.pack(side="left")


load_data()
root.mainloop()
