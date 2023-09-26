import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import paramiko
import sqlite3

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('File manager')
        self.geometry('500x500')
        self.resizable(False, False)
        self.manager = Manager(self)
        self.mainloop()

class Manager(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.filenames = ''
        self.directory = ''
        self.entry_ip = ''
        self.entry_user = ''
        self.entry_password = ''
        self.entry_path = ''

        self.ip_records = ''
        self.user_records= ''
        self.password_records = ''

        self.show_records()
        self.widgets()
        self.create_database()
        

    def widgets(self):
        self.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        open_button_to = ttk.Button(self, text='Open files to send', command=lambda: [self.open_to(), self.scrollbar_to()]) #Button
        open_button_from = ttk.Button(self, text='Open directory to get', command=lambda: [self.open_from(), self.scrollbar_from()]) #Button

        
        send_button_to = ttk.Button(self, text='Send files', command=self.send_to) #Button
        send_button_from = ttk.Button(self, text='Get files', command=self.send_from) #Button


        add_button = ttk.Button(self, text='Add entrys', command=self.add_window) #Button
        delete_button = ttk.Button(self, text='Delete entry', command=self.delete_window) #Button

        ip = ttk.Label(self, text='Internet address:') #Label
        user = ttk.Label(self, text='User name:') #Label
        password = ttk.Label(self, text='Password:') #Label
        path = ttk.Label(self, text='Path:') #Label

        self.directory_label = ttk.Label(self, text='') #Label

        self.entry_ip = ttk.Combobox(self, values=self.ip_records) #Entry
        self.entry_user = ttk.Combobox(self, values=self.user_records) #Entry
        self.entry_password = ttk.Combobox(self, values=self.password_records) #Entry
        self.entry_path = ttk.Entry(self) #Entry


        open_button_to.grid(row=0, column=0, sticky='nswe', columnspan = 2, padx=10, pady=10) #Button
        open_button_from.grid(row=0, column=2, sticky='nswe', columnspan = 2, padx=10, pady=10) #Button

        send_button_to.grid(row=2, column=0, sticky='nsew', columnspan = 2,  padx=10, pady=10) #Button
        send_button_from.grid(row=2, column=2, sticky='nsew', columnspan = 2,  padx=10, pady=10) #Button


        add_button.grid(row=4, column=3, sticky='se',  padx=10, pady=10) #Button
        delete_button.grid(row=4, column=0, sticky='sw',  padx=10, pady=10) #Button


        ip.grid(row=1, column=0, sticky='new', padx=10, pady=10, ) #Label
        user.grid(row=1, column=1, sticky='new', padx=10, pady=10, ) #Label
        password.grid(row=1, column=2, sticky='new', padx=10, pady=10, ) #Label
        path.grid(row=1, column=3, sticky='new', padx=10, pady=10) #Label

        self.directory_label.grid(row=4, column=0, columnspan=3, sticky='nwe', padx=10, pady=10) #Label
        
        self.entry_ip.grid(row=1, column=0, sticky='ew', padx=10, pady=10) #Entry
        self.entry_user.grid(row=1, column=1, sticky='ew', padx=10, pady=10) #Entry
        self.entry_password.grid(row=1, column=2, sticky='ew', padx=10, pady=10) #Entry
        self.entry_path.grid(row=1, column=3, sticky='ew', padx=10, pady=10) #Entry


    def scrollbar_to(self):
        text = tk.Text(self, height=10)
        text.grid(row=3, column=0, sticky='nw', columnspan=4)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=text.yview)
        scrollbar.grid(row=3, column=2, sticky='nes', columnspan=4)
        text.config(yscrollcommand=scrollbar.set)

        for filename in self.filenames:
            text.insert('end', f'{filename}\n')


    def send_to(self):
        ip = self.entry_ip.get()
        user = self.entry_user.get()
        password = self.entry_password.get()
        path = self.entry_path.get()
        if ip or user or password or path:     
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, username=user, password=password)
                for filename in self.filenames:
                    last_element = filename.split('/')
                    last_element = last_element[-1]
                    scp = ssh.open_sftp()
                    scp.put(f'{filename}', f'{path}/{last_element}')
                    scp.close()
                messagebox.showinfo('Succes', f'Success Message: Files moved to: {ip} in: {path} directory!')
            except paramiko.AuthenticationException:
                messagebox.showerror('Error', 'Error Message: Authentication failed. Check your credentials!')
            except paramiko.SSHException as e:
                messagebox.showerror('Error', f'Error Message: SSH connection error: {e}')
            except Exception as e:
                messagebox.showerror('Error', f'Error Message: An error occurred: {e}')
                print(f"An error occurred: {str(e)}")
            finally:
                ssh.close()
        else:
            messagebox.showerror('Error', 'Error Message: Please fill entrys!')


    def open_to(self):
        self.filenames = filedialog.askopenfilenames(
            title='Open a file',
            initialdir='/',
            filetypes=(('All files', '*'),))
        
        
    def open_from(self):
        self.directory = filedialog.askdirectory()
        self.directory_label.config(text = self.directory)
        
    def scrollbar_from(self):
        self.text = tk.Text(self, height=10)
        self.text.grid(row=3, column=0, sticky='nw', columnspan=4)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.text.yview)
        scrollbar.grid(row=3, column=2, sticky='nes', columnspan=4)
        self.text.config(yscrollcommand=scrollbar.set)


    def send_from(self):
        ip = self.entry_ip.get()
        user = self.entry_user.get()
        password = self.entry_password.get()
        path = self.entry_path.get()

        name = self.text.get('1.0', 'end-1c')
        name_list = list(name.split('\n'))
        
        if ip or user or password or path or name_list:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, username=user, password=password)
                for name in name_list:
                    scp = ssh.open_sftp()
                    scp.get(f'{path}/{name}', f'{self.directory}/{name}')
                    scp.close()
                    # messagebox.showinfo('Success', f'Success Message: Files: {name_list} moved to: {self.directory}!')
            except paramiko.AuthenticationException:
                messagebox.showerror('Error', 'Error Message: Authentication failed. Please check your credentials!')
            except paramiko.SSHException as e:
                messagebox.showerror('Error', f'Error Message: SSH connection error: {e}')
            except Exception as e:
                messagebox.showerror('Error', f'Error Message: An error occurred: {e}')
                
                print(f"Error Message: An error occurred: {str(e)}")
            finally:
                ssh.close()
        else:
            messagebox.showerror('Error', 'Error Message: Please fill entrys!')



    def create_database(self):
        if sqlite3.connect('entrys.db'):
            pass
        else:
            connection = sqlite3.connect('entrys.db')
            cursor = connection.cursor()
            cursor.execute("""CREATE TABLE entrys(
                            ip TEXT,
                            user TEXT,
                            password TEXT
                        )""")
            connection.commit()
            connection.close()


    def add_window(self):
        add = ttk.Toplevel(self)
        add.geometry("300x400")
        add.resizable(False, False)
        add.title('Add records')

        add.columnconfigure((0), weight=1, uniform='a')
        add.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')

        ip_label = ttk.Label(add, text='Entry Internet address: ') #Label
        user_label = ttk.Label(add, text='Entry user name: ') #Label
        password_label = ttk.Label(add, text='Entry password: ') #Label

        self.ip_add = ttk.Entry(add) #Entry
        self.user_add = ttk.Entry(add) #Entry
        self.password_add = ttk.Entry(add, show='*') #Entry

        add_button = ttk.Button(add, text='Add', command=lambda: [self.add_records(), self.refresh(), add.destroy()]) #Button

        ip_label.grid(row=0, column=0, sticky='nw', padx=10, pady=10) #Label
        user_label.grid(row=1, column=0, sticky='nw', padx=10, pady=10) #Label
        password_label.grid(row=2, column=0, sticky='nw', padx=10, pady=10) #Label


        self.ip_add.grid(row=0, column=0, sticky='ew', padx=10, pady=10) #Entry
        self.user_add.grid(row=1, column=0, sticky='ew', padx=10, pady=10) #Entry
        self.password_add.grid(row=2, column=0, sticky='ew', padx=10, pady=10) #Entry

        add_button.grid(row=3, column=0, sticky='nesw', padx=10, pady=10) #Button


    def add_records(self):

        ip = self.ip_add.get()
        user = self.user_add.get()
        password = self.password_add.get()

        if ip or user or password:
            connection = sqlite3.connect('entrys.db')
            cursor = connection.cursor()
            cursor.execute("INSERT INTO entrys VALUES (:ip_add, :user_add, :password_add)",
                            {
                                'ip_add': ip,
                                'user_add': user,
                                'password_add': password
                            }
                            )
            connection.commit()
            connection.close()

            self.ip_add.delete(0, END)
            self.user_add.delete(0, END)
            self.password_add.delete(0, END)
            messagebox.showinfo('Success', 'Success Message: Entrys added!')
        else:
            messagebox.showerror('Error', 'Error Message: Please fill entrys!')


    def show_records(self):
        connection = sqlite3.connect('entrys.db')
        cursor = connection.cursor()

        cursor.execute("SELECT *, oid FROM entrys")
        records = cursor.fetchall()
        for record in records:
            self.ip_records += record[0] + "\n"
            self.user_records += record[1] + '\n'
            self.password_records += record[2] + '\n'

        connection.commit()
        connection.close()


    def delete_window(self):
        delete = ttk.Toplevel(self)
        delete.geometry("400x300")
        delete.resizable()
        delete.title('Delete records')

        delete.columnconfigure((0), weight=1, uniform='a')
        delete.rowconfigure((0, 1, 2), weight=1, uniform='a')

        delete_label = ttk.Label(delete, text='Entry row to delete: ') #Label
        self.delete_row = ttk.Entry(delete) #Entry
        del_button = ttk.Button(delete, text='Delete', command=lambda: [self.delete_record(), self.refresh(), delete.destroy()]) #Button

        delete_label.grid(row=0, column=0, sticky='nw', padx=10, pady=10) #Label
        self.delete_row.grid(row=0, column=0, sticky='ew', padx=10, pady=10) #Entry
        del_button.grid(row=2, column=0, sticky='nesw', padx=10, pady=10) #Button


        text = tk.Text(delete, height=10)
        text.grid(row=1, column=0, sticky='nw', columnspan=4)
        scrollbar = ttk.Scrollbar(delete, orient='vertical', command=text.yview)
        scrollbar.grid(row=1, column=0, sticky='nes', columnspan=4)
        text.config(yscrollcommand=scrollbar.set)

        connection = sqlite3.connect('entrys.db')
        cursor = connection.cursor()

        cursor.execute("SELECT *, oid FROM entrys")
        records = cursor.fetchall()
        for record in records:
            text.insert('end', f'ROW -- {record[3]}, IP: {record[0]}, USER: {record[1]}, PASSWORD: {record[2]}\n')

        connection.commit()
        connection.close()

    
    def delete_record(self):
        delete_row = self.delete_row.get()
        if delete_row:
            connection = sqlite3.connect('entrys.db')
            cursor = connection.cursor()

            cursor.execute("SELECT *, oid FROM entrys")
            records = cursor.fetchall()
            for record in records:
                oid = record[3]
            if delete_row in str(oid):
                cursor.execute(f"DELETE from entrys WHERE oid = {delete_row}" )
                messagebox.showinfo('Success', 'Success Message: Entry deleted')
                print('exist')
            else:
                messagebox.showerror('Error', ' Error Message: Please enter a valid row!')
                print('not exist')

            connection.commit()
            connection.close()
        else:
            messagebox.showerror('Error', 'Error Message: Please fill entry')


    def refresh(self):
        self.destroy()
        self.__init__(self.master)

App()
