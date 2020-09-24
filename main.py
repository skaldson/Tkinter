import tkinter as tk
from enum import Enum
from db_cursor import DBCursor

class MainMenu(Enum):
    add = 'Add to phone book'
    delete = 'Delete person from phone book'
    search = 'Search for surname'
    view = 'View phone book'
    quit_app = 'Quit'

class CursorWindow:
    def __init__(self, root):
        self.root = root
        root.title('DB Cursor')
        self.db_cursor = DBCursor()

        self.main_menu = tk.Menu(self.root)
        
        self.edit_cascade = tk.Menu(self.main_menu, tearoff=0)
        self.edit_cascade.add_command(label=MainMenu.add.value, command=self.add_record)
        self.edit_cascade.add_command(label=MainMenu.delete.value, command=self.func)
        self.edit_cascade.add_separator()
        self.main_menu.add_cascade(label='Edit', menu=self.edit_cascade)

        self.search_cascade = tk.Menu(self.main_menu, tearoff=0)
        self.search_cascade.add_command(label=MainMenu.search.value, command=self.func)
        self.search_cascade.add_separator()
        self.main_menu.add_cascade(label='Search', menu=self.search_cascade)

        self.view_cascade = tk.Menu(self.main_menu, tearoff=0)
        self.view_cascade.add_command(label=MainMenu.view.value, command=self.func)
        self.view_cascade.add_separator()
        self.main_menu.add_cascade(label='View', menu=self.view_cascade)

        self.quit_cascade = tk.Menu(self.main_menu, tearoff=0)
        self.quit_cascade.add_command(label=MainMenu.quit_app.value, command=self.func)
        self.quit_cascade.add_separator()
        self.main_menu.add_cascade(label='Quit', menu=self.quit_cascade)
       
        self.root.config(menu=self.main_menu)

    def add_record(self):
        add_window = tk.Toplevel(self.root)

        entry_id = tk.Entry(add_window).config(justify='center')
        entry_firstname = tk.Entry(add_window).config(justify='center')
        entry_surname = tk.Entry(add_window).config(justify='center')
        entry_phone = tk.Entry(add_window).config(justify='center')
        submit_button = tk.Button(add_window, text='Submit Data', command=add_data)

        entry_id.pack()
        entry_firstname.pack()
        entry_surname.pack()
        entry_phone.pack()
        submit_button.pack()
        
        def add_data():
            try:
                user_id = int(entry_id.get())
                user_firstname = entry_firstname.get()
                user_surname = entry_surname.get()
                user_phone = entry_phone.get()

                self.db_cursor.add_to_db(user_id, user_firstname, user_surname, user_phone)
            except ValueError:
                return
    def func(self):
        pass

window = tk.Tk()
my_app = CursorWindow(window)
window.mainloop()

