import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_db():
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_siswa TEXT NOT NULL,
        biologi INTEGER NOT NULL,
        fisika INTEGER NOT NULL,
        inggris INTEGER NOT NULL,
        prediksi_fakultas TEXT NOT NULL)
    """)
    conn.commit()
    conn.close()

create_db()

def prediksi (biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Dapat Ditentukan"

def submit_nilai():
    nama = entry_nama.get().strip()
    try:
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())
    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka.")
        return

    if not nama:
        messagebox.showerror("Error", "Nama siswa tidak boleh kosong.")
        return

    hasil_prediksi = prediksi(bio, fis, ing)

    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, hasil_prediksi))
    conn.commit()
    conn.close()

    messagebox.showinfo("hasil Prediksi", f"Prediksi Fakultas: {hasil_prediksi}")

    entry_nama.delete(0, tk.END)
    entry_bio.delete(0, tk.END)
    entry_fis.delete(0, tk.END)
    entry_ing.delete(0, tk.END)

def on_enter(e):
    btn_submit["bg"] = "#4CAF50"
    btn_submit["fg"] = "white"

def on_leave(e):
    btn_submit["bg"] = "SystemButtonFace"
    btn_submit["fg"] = "black"

root = tk.Tk()
root.title("Input Nilai Siswa")
root.geometry("360x280")
root.resizable(False, False)

label_nama = tk.Label(root, text="Nama Siswa:", font=("Arial", 10))
label_nama.grid(row=0, column=0, padx=15, pady=10, sticky="w")
entry_nama = tk.Entry(root, width=25)
entry_nama.grid(row=0, column=1, padx=15, pady=10)

label_bio = tk.Label(root, text="Nilai Biologi:", font=("Arial", 10))
label_bio.grid(row=1, column=0, padx=15, pady=10, sticky="w")
entry_bio = tk.Entry(root, width=25)
entry_bio.grid(row=1, column=1, padx=15, pady=10)

label_fis = tk.Label(root, text="Nilai Fisika:", font=("Arial", 10))
label_fis.grid(row=2, column=0, padx=15, pady=10, sticky="w")
entry_fis = tk.Entry(root, width=25)
entry_fis.grid(row=2, column=1, padx=15, pady=10)

label_ing = tk.Label(root, text="Nilai Inggris:", font=("Arial", 10))
label_ing.grid(row=3, column=0, padx=15, pady=10, sticky="w")
entry_ing = tk.Entry(root, width=25)
entry_ing.grid(row=3, column=1, padx=15, pady=10)

btn_submit = tk.Button(
    root, 
    text="Submit Nilai", 
    command=submit_nilai, 
    width=15, 
    font=("Arial", 10, "bold"),
    bg="SystemButtonFace",
    fg="black"
)
btn_submit.grid(row=4, column=0, columnspan=2, pady=20)

btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)

root.mainloop()