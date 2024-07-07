from tkinter import *
from tkinter import messagebox
import spa_db as spa_db
import cze_db as cze_db
import main as main
import gui as gui

def change_dictionary(root, lang):
    if lang == 'spa':
        gui.cze_cro(root)
    elif lang == 'cze':
        gui.spa_cro(root)

def delete_entries(entries, lang):
    for entry in entries.values():
        entry.delete(0, END)

    if lang == 'spa':
        entries["Španjolski"].focus()
    elif lang == 'cze':
        entries["Češki"].focus()

def insert_into_entries(entries, values, lang):
    entries["ID"].insert(0, values[0])
    entries["Vrsta riječi"].insert(0, values[2])
    entries["Rod"].insert(0, values[3])
    entries["Hrvatski"].insert(0, values[4])

    if lang == 'spa':
        entries["Španjolski"].insert(0, values[1])
    elif lang == 'cze':
        entries["Češki"].insert(0, values[1])

def select_word(e, treeview, entries, lang):
    delete_entries(entries, lang)
    selected = treeview.focus()
    values = treeview.item(selected, 'values')
    if values:
        insert_into_entries(entries, values, lang)

def delete_word(treeview, entries, lang):
    if lang == 'spa':
        db = spa_db
    elif lang == 'cze':
        db = cze_db
    selected = treeview.selection()[0]
    treeview.delete(selected)
    db.delete_word_from_db(entries["ID"].get())
    delete_entries(entries, lang)

def delete_all(treeview, entries, lang):
    response = messagebox.askyesno("Brisanje rječnika", "Jeste li sigurni da želite izbrisati cijeli rječnik?")
    if lang == 'spa':
        db = spa_db
    elif lang == 'cze':
        db = cze_db

    if response:
        for word in treeview.get_children():
            treeview.delete(word)
        db.delete_all_from_db()
        delete_entries(entries, lang)
        db.create_table()

def update_word(treeview, entries, lang):
    selected = treeview.focus()

    if lang == 'spa':
        treeview.item(selected, text="", values=(
            entries["ID"].get(), entries["Španjolski"].get(), entries["Vrsta riječi"].get(),
            entries["Rod"].get(), entries["Hrvatski"].get()))
        spa_db.update_word_in_db(entries["ID"].get(), entries["Španjolski"].get(), entries["Vrsta riječi"].get(),
                            entries["Rod"].get(), entries["Hrvatski"].get())
    elif lang == 'cze':
        treeview.item(selected, text="", values=(
            entries["ID"].get(), entries["Češki"].get(), entries["Vrsta riječi"].get(),
            entries["Rod"].get(), entries["Češki"].get()))
        cze_db.add_word_to_db(entries["ID"].get(), entries["Češki"].get(), entries["Vrsta riječi"].get(),
                      entries["Rod"].get(), entries["Hrvatski"].get())
    delete_entries(entries, lang)

def add_word(treeview, entries, lang):
    if lang == 'spa':
        spa_db.add_word_to_db(entries["ID"].get(), entries["Španjolski"].get(), entries["Vrsta riječi"].get(),
                      entries["Rod"].get(), entries["Hrvatski"].get())
    elif lang == 'cze':
        cze_db.add_word_to_db(entries["ID"].get(), entries["Češki"].get(), entries["Vrsta riječi"].get(),
                      entries["Rod"].get(), entries["Hrvatski"].get())
    delete_entries(entries, lang)
    clear_treeview_table(treeview)
    populate_treeview(treeview, lang)

def clear_treeview_table(treeview):
    treeview.delete(*treeview.get_children())

def populate_treeview(treeview, lang):
    if lang == 'spa':
        db = spa_db
    elif lang == 'cze':
        db = cze_db

    for word in treeview.get_children():
            treeview.delete(word)

    words = db.query_db()
    for count, record in enumerate(words):
        treeview.insert(parent='', index='end', iid=count, text='', 
                        values=(record[0], record[2], record[3], record[4], record[5]), tags=('row',))
        
def search_words(treeview, lang, search, search_entry):
    if lang == 'spa':
        db = spa_db
    elif lang == 'cze':
        db = cze_db
    
    lookup_record = search_entry.get()
    search.destroy()

    for word in treeview.get_children():
            treeview.delete(word)

    words = db.search_words(lookup_record)
    if not words:
        messagebox.showinfo("Riječ ne postoji", f"Riječ {lookup_record} ne postoji u rječniku.")
    else:
        for count, record in enumerate(words):
            treeview.insert(parent='', index='end', iid=count, text='', 
                            values=(record[0], record[2], record[3], record[4], record[5]), tags=('row',))
        
def count_words(lang):
    if lang == 'spa':
        db = spa_db
    elif lang == 'cze':
        db = cze_db

    count = db.count_words()
    messagebox.showinfo("Broj riječi", f"Ukupno riječi u rječniku: {count}")