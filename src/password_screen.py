from tkinter import ttk, Frame, Label, Entry, Button, LEFT, font
from models.repositories.credentials_repository import CredentialsDatabase
from settings import CREDENTIALS_DB, SALT

import sys
sys.path.append("..")

from providers.password_encrypt_provider import PasswordEncryptProvider


class PasswordPage(Frame):
    def __init__(self, master_password, master=None):
        # Connects to the database
        self.conn = CredentialsDatabase('SQLITE', dbname=CREDENTIALS_DB)
        self.credentials_list = self.get_registered_credentials()

        # Creates the hash provider instance
        self.encrypt_provider = PasswordEncryptProvider(SALT, master_password)

        Frame.__init__(self, master)

        # Create the tabs for the login screen
        self.tabControl = ttk.Notebook(master)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='Create credentials')
        self.tabControl.add(self.tab2, text='Registered credentials')
        self.tabControl.pack(expand=1, fill="both")

        # CREATE CREDENTIALS SCREEN ----------------------------------------
        # Header container
        self.create_credential_header_container = Frame(self.tab1)
        self.create_credential_header_container.pack()
        self.create_credential_header_container['pady'] = 10
        # Header Text
        self.create_credential_header = Label(self.create_credential_header_container, text='Cadastro de credenciais')
        self.create_credential_header.pack()

        # Credential name container
        self.register_credential_name_container = Frame(self.tab1)
        self.register_credential_name_container['pady'] = 10
        self.register_credential_name_container['padx'] = 10
        self.register_credential_name_container.pack()
        # Credential name input and label
        self.register_credential_name_label = Label(self.register_credential_name_container, text='Nome da credencial',
                                                    width=20)
        self.register_credential_name_input = Entry(self.register_credential_name_container)
        self.register_credential_name_label.pack(side=LEFT)
        self.register_credential_name_input.pack()

        # Credential url container
        self.register_credential_url_container = Frame(self.tab1)
        self.register_credential_url_container['pady'] = 10
        self.register_credential_url_container['padx'] = 10
        self.register_credential_url_container.pack()
        # Credential url input and label
        self.register_credential_url_label = Label(self.register_credential_url_container, text='Url da credencial',
                                                   width=20)
        self.register_credential_url_input = Entry(self.register_credential_url_container)
        self.register_credential_url_label.pack(side=LEFT)
        self.register_credential_url_input.pack()

        # Password container
        self.register_credential_password_container = Frame(self.tab1)
        self.register_credential_password_container['pady'] = 10
        self.register_credential_password_container['padx'] = 10
        self.register_credential_password_container.pack()
        # Password input and label
        self.register_credential_password_label = Label(self.register_credential_password_container, text='Senha', width=20)
        self.register_credential_password_input = Entry(self.register_credential_password_container, show="*")
        self.register_credential_password_label.pack(side=LEFT)
        self.register_credential_password_input.pack()

        # Password container
        self.register_confirm_credential_password_container = Frame(self.tab1)
        self.register_confirm_credential_password_container['pady'] = 10
        self.register_confirm_credential_password_container['padx'] = 10
        self.register_confirm_credential_password_container.pack()
        # Password input and label
        self.register_confirm_credential_password_label = Label(self.register_confirm_credential_password_container,
                                                                text='Confirmar senha', width=20)
        self.register_confirm_credential_password_input = Entry(self.register_confirm_credential_password_container,
                                                                show="*")
        self.register_confirm_credential_password_label.pack(side=LEFT)
        self.register_confirm_credential_password_input.pack()

        # Submit button container
        self.register_submit_container = Frame(self.tab1)
        self.register_submit_container.pack()
        self.register_submit_container['pady'] = 10
        # Submit button
        self.register_submit_button = Button(self.register_submit_container)
        self.register_submit_button['text'] = 'Cadastrar credencial'
        self.register_submit_button['command'] = self.register_credential
        self.register_submit_button.pack()

        # Register message container
        self.register_message_container = Frame(self.tab1)
        self.register_message_container['pady'] = 10
        self.register_message_container['padx'] = 10
        self.register_message_container.pack()
        # Register message
        self.register_message = Label(self.register_message_container, text='')
        self.register_message.pack()

        # LIST CREDENTIALS SCREEN ----------------------------------------
        # Header container
        self.list_credential_header_container = Frame(self.tab2)
        self.list_credential_header_container.pack()
        self.list_credential_header_container['pady'] = 10
        # Header Text
        self.list_credential_header = Label(self.list_credential_header_container, text='Credenciais cadastradas')
        self.list_credential_header.pack()

        # Credentials list container
        self.credential_container = Frame(self.tab2)
        self.credential_container['pady'] = 10
        self.credential_container['padx'] = 5
        self.credential_container.pack()
        # Credentials list treeview
        self.credentials_columns = ['Name', 'Url', 'Password']
        self.credentials = ttk.Treeview(columns=self.credentials_columns, show='headings')
        vsb = ttk.Scrollbar(orient='vertical', command=self.credentials.yview)
        hsb = ttk.Scrollbar(orient='horizontal', command=self.credentials.xview)
        self.credentials.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.credentials.grid(column=0, row=0, sticky='nsew', in_=self.credential_container)
        vsb.grid(column=1, row=0, sticky='ns', in_=self.credential_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=self.credential_container)
        self.credential_container.grid_columnconfigure(0, weight=1)
        self.credential_container.grid_rowconfigure(0, weight=1)
        # Builds the credential list
        self.pass_encrypted = False
        self._build_tree(show_pass=self.pass_encrypted)

        # Show pass button container
        self.show_pass_button_container = Frame(self.tab2)
        self.show_pass_button_container.pack()
        self.show_pass_button_container['pady'] = 10
        # Show pass button
        self.show_pass_button = Button(self.show_pass_button_container)
        self.show_pass_button['text'] = 'Show passwords'
        self.show_pass_button['command'] = self.show_passowd
        self.show_pass_button.pack()

    def _build_tree(self, show_pass=False):
        for col in self.credentials_columns:
            self.credentials.heading(col, text=col.title(), command=lambda c=col: self.sortby(self.credentials, c, 0))
            # adjust the column's width to the header string
            self.credentials.column(col, width=font.Font().measure(col.title()))

        self.pass_encrypted = not show_pass
        for credential in self.credentials_list:
            if show_pass:
                decrypted_pass = self.encrypt_provider.decrypt_password(credential.password)
                credential_data = [credential.name, credential.url, decrypted_pass]
            else:
                credential_data = [credential.name, credential.url, credential.password.decode()]

            self.credentials.insert('', 'end', values=credential_data)

            for ix, val in enumerate(credential_data):
                col_w = font.Font().measure(val)
                if self.credentials.column(self.credentials_columns[ix], width=None) < col_w:
                    self.credentials.column(self.credentials_columns[ix], width=col_w)

    def sortby(self, tree, col, descending):
        """sort tree contents when a column header is clicked on"""
        # grab values to sort
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        # if the data to be sorted is numeric change to float
        # data =  change_numeric(data)
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        # switch the heading so it will sort in the opposite direction
        tree.heading(col, command=lambda col=col: self.sortby(tree, col, int(not descending)))

    def register_credential(self):
        credential_name = self.register_credential_name_input.get()
        credential_url = self.register_credential_url_input.get()
        credential_password = self.register_credential_password_input.get()
        credential_confirm_password = self.register_confirm_credential_password_input.get()

        if credential_password != credential_confirm_password:
            self.register_message['text'] = 'Password and password confirmation don\'t match'
            return None

        # Encrypts password
        encrypted_password = self.encrypt_provider.encrypt_password(credential_password)

        # Stores encrypted password in database
        new_credential = self.conn.create_credential(credential_name=credential_name,
                                                     credential_password=encrypted_password,
                                                     credential_url=credential_url)

        if not new_credential:
            self.register_message['text'] = 'Credential already exists'
        else:
            self.register_message['text'] = 'Credential created successfuly'

        self.credentials_list.append(new_credential)
        self._build_tree()

    def get_registered_credentials(self):
        credentials_list = self.conn.get_all_credentials()

        return credentials_list

    def show_passowd(self):
        self.credentials.delete(*self.credentials.get_children())
        self._build_tree(show_pass=self.pass_encrypted)
