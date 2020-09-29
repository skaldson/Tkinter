import tkinter as tk
import sqlite3
import os
from enum import Enum
from db_cursor import DBCursor
from bool_funcs import all_digit


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
        root.geometry('500x300')
        self.db_cursor = DBCursor()
        self.common_frame = tk.Frame(self.root)
        self.__font = ('Arial', 16, 'bold')
        self.__table_font = ('Times Mew Roman', 10, 'bold')
        self.__value_error = 'You have one or several not an integer value type'
        self.__unique_value = 'UNIQUE constraint failed: Names.ID'

        try:
            self.db_have_records = self.get_db_data()
            if self.db_have_records:
                self.init_menu()
            else:
                self.start_msg_box('DB doesn\'t have any records!!!')
                self.init_button()
        except sqlite3.OperationalError:
            self.start_msg_box('DB doesn\'t have `Names` table')
            self.init_button()

    def start_msg_box(self, message):
        self.db_is_empty = tk.Message(self.common_frame, fg='red', font=self.__font, width=200)
        self.db_is_empty.config(text=message)
        self.db_is_empty.pack()
        self.common_frame.pack()

    def get_db_data(self):
        return self.db_cursor.view_all_data()

    def init_button(self):
        self.initialize_button = tk.Button(self.common_frame, text='Init Data', command=self.init_db)
        self.initialize_button.pack(anchor=tk.S)
        self.common_frame.pack()
        # self.root.update()

    def init_db(self):
        script_name = 'init_db.py'
        os.system(f'python3 {script_name}')

    def init_menu(self):
        self.main_menu = tk.Menu(self.root)
        
        self.edit_cascade = tk.Menu(self.main_menu, tearoff=0)
        self.edit_cascade.add_command(label=MainMenu.add.value, command=self.add_record)
        self.edit_cascade.add_command(label=MainMenu.delete.value, command=self.delete_record)
        self.edit_cascade.add_separator()
        self.main_menu.add_cascade(label='Edit', menu=self.edit_cascade)

        self.search_cascade = tk.Menu(self.main_menu, tearoff=0)
        self.search_cascade.add_command(label=MainMenu.search.value, command=self.search_record)
        self.search_cascade.add_separator()
        self.main_menu.add_cascade(label='Search', menu=self.search_cascade)

        self.view_cascade = tk.Menu(self.main_menu, tearoff=0)
        self.view_cascade.add_command(label=MainMenu.view.value, command=self.view_data)
        self.view_cascade.add_separator()
        self.main_menu.add_cascade(label='View', menu=self.view_cascade)

        self.quit_cascade = tk.Menu(self.main_menu, tearoff=0)
        self.quit_cascade.add_command(label=MainMenu.quit_app.value, command=exit)
        self.quit_cascade.add_separator()
        self.main_menu.add_cascade(label='Quit', menu=self.quit_cascade)
        
        self.root.config(menu=self.main_menu)

    def add_record(self):
        self.toplevel_add = tk.Toplevel(self.root)
        self.frame_id = tk.Frame(self.toplevel_add)
        self.user_id_label = tk.Label(self.frame_id, text='ID')
        self.user_id = tk.Entry(self.frame_id)
        self.user_id.config(justify='center')
        self.user_id_label.pack(anchor=tk.NW)
        self.user_id.pack(anchor=tk.NE)
        self.frame_id.pack()

        self.frame_firstname = tk.Frame(self.toplevel_add)
        self.firstname_label = tk.Label(self.frame_firstname, text='First Name')
        self.firstname = tk.Entry(self.frame_firstname)
        self.firstname.config(justify='center')
        self.firstname_label.pack(anchor=tk.W)
        self.firstname.pack(anchor=tk.E)
        self.frame_firstname.pack()

        self.frame_surname = tk.Frame(self.toplevel_add)
        self.surname_label = tk.Label(self.frame_surname , text='Surname')
        self.surname  = tk.Entry(self.frame_surname)
        self.surname.config(justify='center')
        self.surname_label.pack(anchor=tk.SW)
        self.surname.pack(anchor=tk.SE)
        self.frame_surname.pack()

        self.frame_phone = tk.Frame(self.toplevel_add)
        self.phone_label = tk.Label(self.frame_phone , text='Phone')
        self.phone  = tk.Entry(self.frame_phone)
        self.phone.config(justify='center')
        self.phone_label.pack(anchor=tk.SW)
        self.phone.pack(anchor=tk.SE) 
        self.submit_button = tk.Button(self.frame_phone, text='Submit Data')
        self.submit_button.config(command=self.add_data)
        self.submit_button.pack(anchor=tk.S)
        self.frame_phone.pack(side=tk.BOTTOM)

    def add_data(self):
        # self.reinit_frame()
        try:
            id_val = int(self.user_id.get())
            first_val = self.firstname.get()
            surname_val = self.surname.get()
            phone_val = self.phone.get()
            empty_condition = (id_val) and first_val and surname_val and all_digit(phone_val)
            if empty_condition:
                id_val = int(id_val)
                self.db_cursor.add_to_db(id_val, first_val, surname_val, phone_val)
                sucess_str = 'Record: `%d %s %s %s` was added' % (id_val, first_val, surname_val, phone_val)
                self.output_message(sucess_str, False)
            else:
                self.output_message('Incorrect data, please, check all fields', True)
        except ValueError:
            self.output_message(self.__value_error, True)
        except sqlite3.IntegrityError:
            self.output_message(self.__unique_value, True)
        

    def search_record(self):
        # self.reinit_frame()
        self.toplevel_search = tk.Toplevel(self.root)
        self.search_label = tk.Label(self.toplevel_search, text='Surname')
        self.search = tk.Entry(self.toplevel_search)
        self.search_label.pack(anchor=tk.NW)
        self.search.pack(anchor=tk.NE)

        self.submit_button = tk.Button(self.toplevel_search, text='Submit Data', command=self.search_data)
        self.submit_button.pack(anchor=tk.S)

    def make_table(self, search_result):
        rows = len(search_result)
        columns = len(search_result[0])
        search_result.insert(0, ['ID', 'First Name', 'Surname', 'Phone Number'])
        self.root.geometry('750x300')
        for i in range(rows+1):
            for j in range(columns):
                self.my_entry = tk.Entry(self.common_frame, fg='blue', width=20, font=self.__table_font)
                self.my_entry.grid(row=i, column=j)
                self.my_entry.insert(tk.END, search_result[i][j])
        self.common_frame.pack()

    def search_data(self):
        self.reinit_frame()
        surname_val = self.search.get()
        search_result = self.db_cursor.search_in_db(surname_val)

        if search_result:
            self.make_table(search_result)
        else:
            search_fail_msg = 'Records with %s surname not found' % (surname_val)
            self.output_message(search_fail_msg, True)

    def view_data(self):
        search_result = self.db_cursor.view_all_data()
        self.reinit_frame()
        if search_result:
            self.make_table(search_result)
        else:
            self.output_message('DB is empty!', True)

    def delete_record(self):
        self.toplevel_delete = tk.Toplevel(self.root)
        self.frame_delete = tk.Frame(self.toplevel_delete)
        self.delete_label = tk.Label(self.frame_delete, text='ID')
        self.delete = tk.Entry(self.frame_delete)
        self.delete.config(justify='center')
        self.delete_button = tk.Button(self.frame_delete, text='Submit Data', command=self.delete_data)
        self.delete_all_records = tk.Button(self.frame_delete, text='Delete All Records', command=self.db_cursor.delete_all_records)
        self.delete_drop_table = tk.Button(self.frame_delete, text='Drop Table', command=self.db_cursor.drop_table)

        self.delete_label.pack(anchor=tk.NW)
        self.delete.pack(anchor=tk.NE)
        self.delete_button.pack(anchor=tk.S)
        self.delete_all_records.pack(anchor=tk.S)
        self.delete_drop_table.pack(anchor=tk.S)
        self.frame_delete.pack()

    def reinit_frame(self):
        self.common_frame.destroy()
        self.common_frame = tk.Frame(self.root)

    def output_message(self, message, bad):
        if bad:
            self.info_message = tk.Message(self.common_frame, fg='red', 
                                                    text=message, font=self.__font, width=350)
        else:
            self.info_message = tk.Message(self.common_frame, fg='green', 
                                                    text=message, font=self.__font, width=350)
        self.info_message.pack()
        self.common_frame.pack()

    def delete_data(self):
        self.reinit_frame()
        try:
            user_id = int(self.delete.get())
            if user_id:
                result_msg = self.db_cursor.delete_from_db(user_id)
                if result_msg == 'Failure':
                    delete_fail_msg = '%s: record with %d `ID` not found' % (result_msg, user_id)
                    self.output_message(delete_fail_msg, True)
                elif result_msg[0] == 'Sucess':
                    delete_sucess_msg = f'{result_msg[0]}: record {result_msg[-1]} was deleted'
                    self.output_message(delete_sucess_msg, False)
        except ValueError:
            self.output_message(self.__value_error, True)

def main():
    window = tk.Tk()
    my_app = CursorWindow(window)
    window.mainloop()

main()
