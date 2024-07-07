from tkinter import *
from tkinter import ttk
import event_handling as events
import main as main
import spa_db as spa_db
import cze_db as cze_db

import math

def first_menu():
    root = Tk()
    root.title("Odabir rječnika")

    width = 300
    height = 200
    dim = str(width) + "x" + str(height)
    root.geometry(dim)

    x = width / 6
    y = math.floor(height / 2.666666666666)

    button_frame = Frame(root)
    button_frame.place(x=x, y=y)

    button_spa = Button(button_frame, text="Španjolsko-hrvatski", command=lambda:spa_cro(root))
    button_spa.pack(side='left')

    button_cze = Button(button_frame, text="Češko-hrvatski", command=lambda:cze_cro(root))
    button_cze.pack(side='left')
    
    root.mainloop()

def set_db(root, label, clicked):
        click = clicked.get()
        label.config(text=click)
        db_name = label.cget("text")

        if db_name == "Špa-Hrv":
            spa_cro(root)
        elif db_name == "Češ-Hrv":
            cze_cro(root)

def spa_cro(root):
    lang = "spa"
    root.destroy()
    root_spa_cro = Tk()
    root_spa_cro.title("Španjolsko-hrvatski rječnik")
    root_spa_cro.geometry("700x600")
    spa_db.create_table
    _ = setup_gui(root_spa_cro, lang)
    root_spa_cro.mainloop()

def cze_cro(root):
    lang = "cze"
    root.destroy()
    root_cze_cro = Tk()
    root_cze_cro.title("Češko-hrvatski rječnik")
    root_cze_cro.geometry("700x600")
    cze_db.create_table
    _ = setup_gui(root_cze_cro, lang)
    root_cze_cro.mainloop()

def setup_style():
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="white")
    style.map('Treeview', background=[('selected', "#347083")])

def setup_treeview(tree_frame, lang):
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    treeview = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    treeview.pack()
    tree_scroll.config(command=treeview.yview)

    if lang == "spa":

        treeview['columns'] = ("ID", "Španjolski", "Vrsta riječi", "Rod", "Hrvatski")
        treeview['displaycolumns'] = ("Španjolski", "Vrsta riječi", "Rod", "Hrvatski")
    
        treeview.column("#0", width=0, stretch=NO)
        treeview.column("ID", anchor=W, width=0)
        treeview.column("Španjolski", anchor=W, width=230)
        treeview.column("Vrsta riječi", anchor=W, width=100)
        treeview.column("Rod", anchor=W, width=100)
        treeview.column("Hrvatski", anchor=W, width=250)

        treeview.heading("#0", text="", anchor=W)
        treeview.heading("ID", text="ID", anchor=CENTER)
        treeview.heading("Španjolski", text="Španjolski", anchor=CENTER)
        treeview.heading("Vrsta riječi", text="Vrsta riječi", anchor=CENTER)
        treeview.heading("Rod", text="Rod", anchor=CENTER)
        treeview.heading("Hrvatski", text="Hrvatski", anchor=CENTER)
        
        treeview.tag_configure('row', background='lightblue')

    elif lang == "cze":

        treeview['columns'] = ("ID", "Češki", "Vrsta riječi", "Rod", "Hrvatski")
        treeview['displaycolumns'] = ("Češki", "Vrsta riječi", "Rod", "Hrvatski")
    
        treeview.column("#0", width=0, stretch=NO)
        treeview.column("ID", anchor=W, width=0)
        treeview.column("Češki", anchor=W, width=230)
        treeview.column("Vrsta riječi", anchor=W, width=100)
        treeview.column("Rod", anchor=W, width=100)
        treeview.column("Hrvatski", anchor=W, width=250)

        treeview.heading("#0", text="", anchor=W)
        treeview.heading("ID", text="ID", anchor=CENTER)
        treeview.heading("Češki", text="Češki", anchor=CENTER)
        treeview.heading("Vrsta riječi", text="Vrsta riječi", anchor=CENTER)
        treeview.heading("Rod", text="Rod", anchor=CENTER)
        treeview.heading("Hrvatski", text="Hrvatski", anchor=CENTER)
        
        treeview.tag_configure('row', background='lightblue')
    return treeview

def setup_add_word_frame(root, lang):
    add_word_frame = LabelFrame(root, text="Riječi")
    add_word_frame.pack(fill="x", expand="yes", padx=20)

    if lang == 'spa':
        labels = ["Španjolski", "Vrsta riječi", "Rod", "Hrvatski"]
        entries = {}
    elif lang == 'cze':
        labels = ["Češki", "Vrsta riječi", "Rod", "Hrvatski"]
        entries = {}

    for i, label in enumerate(labels):
        lbl = Label(add_word_frame, text=label)
        lbl.grid(row=i, column=0, padx=10, pady=10)
        entry = Entry(add_word_frame)
        entry.grid(row=i, column=1, padx=10, pady=10)
        entries[label] = entry

    id_entry = Entry(add_word_frame)
    id_entry.place(anchor="nw", x=0, y=0, width=0, height=0)
    entries["ID"] = id_entry

    return add_word_frame, entries

def setup_menus(root, treeview, lang):
    my_menu = Menu(root)
    root.config(menu=my_menu)

    option_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Opcije", menu=option_menu)
    option_menu.add_command(label="Zamijeni rječnik", command=lambda:events.change_dictionary(root, lang))
    option_menu.add_separator()

    search_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Pretraži", menu=search_menu)
    search_menu.add_command(label="Pretraži", command=lambda:setup_search_words(root, treeview, lang))
    search_menu.add_separator()

    search_menu.add_command(label="Reset", command=lambda:events.populate_treeview(treeview, lang))

def setup_search_words(root, treeview, lang):
    search = Toplevel(root)
    search.title("Pretraži riječ")
    search.geometry("400x200")

    search_frame = LabelFrame(search, text="Riječ")
    search_frame.pack(padx=10, pady=10)

    search_entry = Entry(search_frame, font=("Helvetica", 16))
    search_entry.pack(pady=20, padx=20)
    search_entry.focus()
    search_entry.bind('<Return>', lambda event: events.search_words(treeview, lang, search, search_entry))

    search_button = Button(search, text="Pretraži", command=lambda:events.search_words(treeview, lang, search, search_entry))
    search_button.pack(padx=20, pady=20)

def bind_return_key(entries, command):
    for entry in entries.values():
        entry.bind('<Return>', lambda event: command())

def setup_gui(root, lang):
    setup_style()
    
    tree_frame = Frame(root)
    tree_frame.pack(pady=10)
    treeview = setup_treeview(tree_frame, lang)

    setup_menus(root, treeview, lang)

    add_word_frame, entries = setup_add_word_frame(root, lang)

    add_word_button = Button(add_word_frame, text="Dodaj riječ", command=lambda: events.add_word(treeview, entries, lang))
    add_word_button.grid(row=0, column=2, padx=10, pady=10)
    bind_return_key(entries, lambda: events.add_word(treeview, entries, lang))

    edit_word_button = Button(add_word_frame, text="Uredi riječ", command=lambda: events.update_word(treeview, entries, lang))
    edit_word_button.grid(row=1, column=2, padx=10, pady=10)

    delete_word_button = Button(add_word_frame, text="Izbriši riječ", command=lambda: events.delete_word(treeview, entries, lang))
    delete_word_button.grid(row=2, column=2, padx=10, pady=10)

    delete_all_button = Button(add_word_frame, text="Izbriši sve riječi", command=lambda: events.delete_all(treeview, entries, lang))
    delete_all_button.grid(row=3, column=2, padx=10, pady=10)

    count_words_button = Button(add_word_frame, text="Broj riječi", command=lambda: events.count_words(lang))
    count_words_button.grid(row=0, column=3, padx=10, pady=10)

    clear_entries = Button(add_word_frame, text="Očisti polja", command=lambda:events.delete_entries(entries, lang))
    clear_entries.grid(row=1, column=3, padx=10, pady=10)

    treeview.bind("<ButtonRelease-1>", lambda e: events.select_word(e, treeview, entries, lang))

    events.populate_treeview(treeview, lang)

    return treeview